# Konsult-Sök MCP Server

MCP-server för att söka konsultuppdrag bland Stockholms 10 största konsultmäklare.
Stödjer filtrering på plats och timpris.

## Plattformar

| Plattform | Beskrivning |
|-----------|-------------|
| Upgraded | IT och Management konsultuppdrag |
| Tech Relations | Tech-fokuserade konsultuppdrag |
| Wise IT | IT-konsultuppdrag |
| Ework | Skandinaviens största konsultmäklare |
| Brainville | IT-konsultuppdrag i Stockholm |
| Experis | IT och tech-rekrytering |
| Randstad | Konsult och rekrytering |
| Academic Work | Young professionals och konsulter |
| Manpower | Bemanning och konsulttjänster |
| Cinode | Konsultplattform och nätverk |

## Platser

Stockholm, Göteborg, Malmö, Uppsala, Linköping, Örebro, Västerås, Helsingborg,
Norrköping, Jönköping, Umeå, Lund, Borås, Sundsvall, Gävle, Remote, Distans

## Installation

```bash
cd /Users/spjutbjorn/git/pythonTools/mcp/konsult-sok
pip install -r requirements.txt
```

## Verktyg

### search_konsult
Sök konsultuppdrag på alla eller utvalda plattformar med valfria filter.

**Parametrar:**
- `query` (required): Sökterm, t.ex. "Python", "DevOps", "Projektledare"
- `location` (optional): Plats/stad, t.ex. "Stockholm", "Göteborg", "Remote"
- `min_price` (optional): Minsta timpris i SEK (t.ex. 800)
- `max_price` (optional): Högsta timpris i SEK (t.ex. 1200)
- `platforms` (optional): Lista av plattformar att söka på

**Exempel:**
```
search_konsult(query="Python utvecklare")
search_konsult(query="DevOps", location="Stockholm")
search_konsult(query="Java", min_price=900, max_price=1100)
search_konsult(query="Projektledare", location="Göteborg", platforms=["upgraded", "ework"])
```

### list_platforms
Lista alla tillgängliga konsultplattformar.

### list_locations
Lista alla tillgängliga platser/städer.

### get_platform_url
Få direktlänk till en plattforms uppdragssida.

**Parametrar:**
- `platform` (required): Plattforms-ID
- `query` (optional): Sökterm
- `location` (optional): Plats
