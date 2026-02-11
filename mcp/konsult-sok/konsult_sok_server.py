#!/usr/bin/env python3
"""
MCP Server for searching consulting jobs in Stockholm.
Searches the top consulting brokers/platforms in the Stockholm area.
"""

import os
import sys
import asyncio
import json
import aiohttp
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote_plus
import re

# Add parent directory to path to import mcp_common
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.server import Server
import mcp.types as types
from mcp_common import create_text_response, create_error_response, run_mcp_server, safe_get_arg, MCPToolBuilder

# Swedish locations/cities
LOCATIONS = [
    "Stockholm", "Göteborg", "Malmö", "Uppsala", "Linköping", "Örebro",
    "Västerås", "Helsingborg", "Norrköping", "Jönköping", "Umeå", "Lund",
    "Borås", "Sundsvall", "Gävle", "Remote", "Distans"
]

# Consulting platforms in Stockholm
PLATFORMS = {
    "upgraded": {
        "name": "Upgraded",
        "base_url": "https://upgraded.se",
        "search_url": "https://upgraded.se/konsultuppdrag/?search={query}",
        "location_param": "&location={location}",
        "description": "IT och Management konsultuppdrag"
    },
    "techrelations": {
        "name": "Tech Relations",
        "base_url": "https://www.techrelations.se",
        "search_url": "https://www.techrelations.se/konsultuppdrag?search={query}",
        "location_param": "&city={location}",
        "description": "Tech-fokuserade konsultuppdrag"
    },
    "wiseit": {
        "name": "Wise IT",
        "base_url": "https://www.wiseit.se",
        "search_url": "https://www.wiseit.se/lediga-uppdrag/?s={query}",
        "location_param": "&location={location}",
        "description": "IT-konsultuppdrag"
    },
    "ework": {
        "name": "Ework",
        "base_url": "https://www.eworkgroup.com",
        "search_url": "https://www.eworkgroup.com/se/konsult/lediga-uppdrag?q={query}",
        "location_param": "&location={location}",
        "description": "Skandinaviens största konsultmäklare"
    },
    "brainville": {
        "name": "Brainville",
        "base_url": "https://brainville.com",
        "search_url": "https://brainville.com/uppdrag/?search={query}",
        "location_param": "&city={location}",
        "description": "IT-konsultuppdrag i Stockholm"
    },
    "experis": {
        "name": "Experis",
        "base_url": "https://www.experis.se",
        "search_url": "https://www.experis.se/sv/karriar/lediga-jobb?q={query}",
        "location_param": "&location={location}",
        "description": "IT och tech-rekrytering"
    },
    "randstad": {
        "name": "Randstad",
        "base_url": "https://www.randstad.se",
        "search_url": "https://www.randstad.se/lediga-jobb/?keywords={query}",
        "location_param": "&location={location}",
        "description": "Konsult och rekrytering"
    },
    "academicwork": {
        "name": "Academic Work",
        "base_url": "https://www.academicwork.se",
        "search_url": "https://www.academicwork.se/lediga-jobb?query={query}",
        "location_param": "&city={location}",
        "description": "Young professionals och konsulter"
    },
    "manpower": {
        "name": "Manpower",
        "base_url": "https://www.manpower.se",
        "search_url": "https://www.manpower.se/lediga-jobb?q={query}",
        "location_param": "&l={location}",
        "description": "Bemanning och konsulttjänster"
    },
    "cinode": {
        "name": "Cinode (Konsultkartan)",
        "base_url": "https://cinode.com",
        "search_url": "https://cinode.com/market?search={query}",
        "location_param": "&location={location}",
        "description": "Konsultplattform och nätverk"
    }
}

# Cache for search results
CACHE_FILE = Path(__file__).parent / "search_cache.json"
search_cache = {}


def load_cache():
    """Load search cache from file."""
    global search_cache
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                search_cache = json.load(f)
        except:
            search_cache = {}


def save_cache():
    """Save search cache to file."""
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(search_cache, f, ensure_ascii=False, indent=2)


async def fetch_url(session: aiohttp.ClientSession, url: str) -> str:
    """Fetch URL content with proper headers."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'sv-SE,sv;q=0.9,en;q=0.8',
    }
    try:
        async with session.get(url, headers=headers, timeout=15) as response:
            if response.status == 200:
                return await response.text()
    except Exception as e:
        pass
    return ""


def extract_price(text: str) -> int | None:
    """Extract hourly rate from text. Returns SEK/hour or None."""
    if not text:
        return None

    # Common patterns for hourly rates in Swedish
    patterns = [
        r'(\d[\d\s]*)\s*(?:kr|sek|:-)\s*/?\s*(?:tim|h|hour)',  # 850 kr/tim, 850:-/h
        r'(\d[\d\s]*)\s*(?:kr|sek|:-)\s*/?\s*(?:timme|timmar)',  # 850 kr/timme
        r'timpris[:\s]*(\d[\d\s]*)',  # timpris: 850
        r'timarvode[:\s]*(\d[\d\s]*)',  # timarvode 850
        r'(\d{3,4})\s*-\s*(\d{3,4})\s*(?:kr|sek)',  # 800-1000 kr (range)
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # Handle range (take average)
            if len(match.groups()) == 2 and match.group(2):
                low = int(match.group(1).replace(' ', ''))
                high = int(match.group(2).replace(' ', ''))
                return (low + high) // 2
            # Single value
            price_str = match.group(1).replace(' ', '')
            price = int(price_str)
            # Sanity check for hourly rates (typically 500-2000 SEK)
            if 300 <= price <= 3000:
                return price

    return None


def parse_generic_jobs(html: str, base_url: str, platform_name: str) -> list[dict]:
    """Generic parser for job listings."""
    jobs = []
    if not html:
        return jobs

    soup = BeautifulSoup(html, 'html.parser')

    # Common patterns for job listings
    selectors = [
        'article', '.job-listing', '.job-item', '.uppdrag', '.assignment',
        '.vacancy', '[class*="job"]', '[class*="uppdrag"]', '.card',
        'li[class*="job"]', 'div[class*="listing"]'
    ]

    for selector in selectors:
        items = soup.select(selector)[:10]  # Limit to 10 per selector
        for item in items:
            # Try to find title
            title_elem = item.select_one('h2, h3, h4, .title, [class*="title"], a')
            if not title_elem:
                continue

            title = title_elem.get_text(strip=True)
            if len(title) < 5 or len(title) > 200:
                continue

            # Try to find link
            link_elem = item.select_one('a[href]') or title_elem if title_elem.name == 'a' else None
            link = ""
            if link_elem and link_elem.get('href'):
                link = urljoin(base_url, link_elem['href'])

            # Try to find description
            desc_elem = item.select_one('p, .description, [class*="desc"], .excerpt')
            description = desc_elem.get_text(strip=True)[:200] if desc_elem else ""

            # Try to find location
            loc_elem = item.select_one('[class*="location"], [class*="plats"], .city')
            location = loc_elem.get_text(strip=True) if loc_elem else ""

            # Try to find price/rate
            price_elem = item.select_one('[class*="price"], [class*="rate"], [class*="pris"], [class*="arvode"]')
            item_text = item.get_text()
            price = extract_price(price_elem.get_text() if price_elem else item_text)

            jobs.append({
                "title": title,
                "link": link,
                "description": description,
                "location": location,
                "price": price,  # SEK/hour or None
                "platform": platform_name
            })

        if jobs:
            break  # Found jobs with this selector

    return jobs[:10]  # Limit results


async def search_platform(
    session: aiohttp.ClientSession,
    platform_id: str,
    query: str,
    location: str = None
) -> list[dict]:
    """Search a specific platform for jobs."""
    if platform_id not in PLATFORMS:
        return []

    platform = PLATFORMS[platform_id]
    search_url = platform["search_url"].format(query=quote_plus(query))

    # Add location parameter if specified
    if location and "location_param" in platform:
        search_url += platform["location_param"].format(location=quote_plus(location))

    html = await fetch_url(session, search_url)
    jobs = parse_generic_jobs(html, platform["base_url"], platform["name"])

    # If parsing fails, return direct link to search
    if not jobs:
        jobs = [{
            "title": f"Sök '{query}' på {platform['name']}",
            "link": search_url,
            "description": platform["description"],
            "location": location or "",
            "price": None,
            "platform": platform["name"]
        }]

    return jobs


def filter_jobs_by_price(jobs: list[dict], min_price: int = None, max_price: int = None) -> list[dict]:
    """Filter jobs by hourly rate."""
    if min_price is None and max_price is None:
        return jobs

    filtered = []
    for job in jobs:
        price = job.get("price")
        if price is None:
            # Include jobs without price info
            filtered.append(job)
            continue

        if min_price and price < min_price:
            continue
        if max_price and price > max_price:
            continue
        filtered.append(job)

    return filtered


def filter_jobs_by_location(jobs: list[dict], location: str) -> list[dict]:
    """Filter jobs by location."""
    if not location:
        return jobs

    location_lower = location.lower()
    filtered = []
    for job in jobs:
        job_location = job.get("location", "").lower()
        # Include if location matches or job has no location specified
        if not job_location or location_lower in job_location or job_location in location_lower:
            filtered.append(job)

    return filtered


async def search_all_platforms(
    query: str,
    platforms: list[str] = None,
    location: str = None,
    min_price: int = None,
    max_price: int = None
) -> dict:
    """Search all or specified platforms with optional filters."""
    if platforms is None:
        platforms = list(PLATFORMS.keys())

    results = {
        "query": query,
        "location": location,
        "price_range": {"min": min_price, "max": max_price},
        "timestamp": datetime.now().isoformat(),
        "platforms": {},
        "total_jobs": 0
    }

    async with aiohttp.ClientSession() as session:
        tasks = [search_platform(session, p, query, location) for p in platforms if p in PLATFORMS]
        platform_results = await asyncio.gather(*tasks)

        for platform_id, jobs in zip(platforms, platform_results):
            if platform_id in PLATFORMS:
                # Apply filters
                jobs = filter_jobs_by_location(jobs, location)
                jobs = filter_jobs_by_price(jobs, min_price, max_price)

                results["platforms"][platform_id] = {
                    "name": PLATFORMS[platform_id]["name"],
                    "jobs": jobs,
                    "count": len(jobs)
                }
                results["total_jobs"] += len(jobs)

    return results


# Create MCP Server
server = Server("konsult-sok")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        MCPToolBuilder.create_tool(
            name="search_konsult",
            description="Sök konsultuppdrag bland Stockholms största konsultmäklare. Söker på 10 plattformar samtidigt. Stödjer filtrering på plats och timpris.",
            properties={
                "query": {
                    "type": "string",
                    "description": "Sökterm, t.ex. 'Python', 'DevOps', 'Projektledare', 'Java utvecklare'"
                },
                "location": {
                    "type": "string",
                    "description": f"Plats/stad att söka i. Exempel: {', '.join(LOCATIONS[:5])}, Remote"
                },
                "min_price": {
                    "type": "integer",
                    "description": "Minsta timpris i SEK (t.ex. 800)"
                },
                "max_price": {
                    "type": "integer",
                    "description": "Högsta timpris i SEK (t.ex. 1200)"
                },
                "platforms": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": f"Valfritt: Lista av plattformar att söka på. Tillgängliga: {', '.join(PLATFORMS.keys())}"
                }
            },
            required=["query"]
        ),
        MCPToolBuilder.create_tool(
            name="list_platforms",
            description="Lista alla tillgängliga konsultplattformar och deras beskrivningar.",
            properties={},
            required=[]
        ),
        MCPToolBuilder.create_tool(
            name="list_locations",
            description="Lista alla tillgängliga platser/städer att söka i.",
            properties={},
            required=[]
        ),
        MCPToolBuilder.create_tool(
            name="get_platform_url",
            description="Få direktlänk till en konsultplattforms uppdragssida.",
            properties={
                "platform": {
                    "type": "string",
                    "description": f"Plattform: {', '.join(PLATFORMS.keys())}"
                },
                "query": {
                    "type": "string",
                    "description": "Valfri sökterm"
                },
                "location": {
                    "type": "string",
                    "description": "Valfri plats"
                }
            },
            required=["platform"]
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    """Handle tool calls."""

    if name == "search_konsult":
        query = safe_get_arg(arguments, "query", "")
        if not query:
            return create_error_response("Sökterm (query) krävs")

        location = safe_get_arg(arguments, "location", None)
        min_price = safe_get_arg(arguments, "min_price", None)
        max_price = safe_get_arg(arguments, "max_price", None)
        platforms = safe_get_arg(arguments, "platforms", None)

        results = await search_all_platforms(query, platforms, location, min_price, max_price)

        # Format output
        output = [f"# Konsultuppdrag: '{query}'"]

        # Show active filters
        filters = []
        if location:
            filters.append(f"Plats: {location}")
        if min_price or max_price:
            price_str = f"{min_price or '?'}-{max_price or '?'} kr/tim"
            filters.append(f"Pris: {price_str}")
        if filters:
            output.append(f"**Filter:** {', '.join(filters)}")

        output.append(f"Sökte {len(results['platforms'])} plattformar, hittade {results['total_jobs']} resultat\n")

        for platform_id, data in results["platforms"].items():
            output.append(f"\n## {data['name']} ({data['count']} träffar)")
            for job in data["jobs"][:5]:  # Show top 5 per platform
                output.append(f"\n### {job['title']}")
                if job.get('location'):
                    output.append(f"📍 {job['location']}")
                if job.get('price'):
                    output.append(f"💰 {job['price']} kr/tim")
                if job.get('description'):
                    output.append(f"{job['description']}")
                if job.get('link'):
                    output.append(f"[Länk]({job['link']})")

        return create_text_response("\n".join(output))

    elif name == "list_platforms":
        output = ["# Konsultplattformar i Stockholm\n"]
        for platform_id, platform in PLATFORMS.items():
            output.append(f"## {platform['name']} (`{platform_id}`)")
            output.append(f"- {platform['description']}")
            output.append(f"- URL: {platform['base_url']}\n")
        return create_text_response("\n".join(output))

    elif name == "list_locations":
        output = ["# Tillgängliga platser\n"]
        output.append("Följande platser kan användas för att filtrera sökresultat:\n")
        for loc in LOCATIONS:
            output.append(f"- {loc}")
        output.append("\n*Tips: Använd 'Remote' eller 'Distans' för att hitta distansuppdrag.*")
        return create_text_response("\n".join(output))

    elif name == "get_platform_url":
        platform_id = safe_get_arg(arguments, "platform", "")
        query = safe_get_arg(arguments, "query", "")
        location = safe_get_arg(arguments, "location", "")

        if platform_id not in PLATFORMS:
            return create_error_response(f"Okänd plattform: {platform_id}. Tillgängliga: {', '.join(PLATFORMS.keys())}")

        platform = PLATFORMS[platform_id]
        if query:
            url = platform["search_url"].format(query=quote_plus(query))
            if location and "location_param" in platform:
                url += platform["location_param"].format(location=quote_plus(location))
        else:
            url = platform["base_url"]

        return create_text_response(f"**{platform['name']}**\n{platform['description']}\n\nURL: {url}")

    return create_error_response(f"Okänt verktyg: {name}")


async def main():
    """Run the MCP server."""
    load_cache()
    await run_mcp_server(server, "konsult-sok", "1.0.0")


if __name__ == "__main__":
    asyncio.run(main())
