# Skapa en ny MCP-server med mcp_common

En steg-för-steg guide för att bygga nya MCP-servrar med återanvändbara komponenter.

## Översikt

`mcp_common.py` tillhandahåller färdiga byggblock för MCP-servrar:

- **create_text_response()** - Skapa standardiserade textsvar
- **create_error_response()** - Skapa standardiserade felsvar
- **run_mcp_server()** - Kör en MCP-server med standardkonfiguration
- **safe_get_arg()** - Säker argumenthämtning från verktygsanrop
- **MCPToolBuilder** - Hjälpklass för att bygga verktyg

## Snabbstart: Skapa en ny server

### Steg 1: Skapa projekt-folder

```bash
cd /Users/spjutbjorn/git/pythonTools/mcp
mkdir min-nya-server
cd min-nya-server
```

### Steg 2: Skapa serverfilen

Skapa `min_server.py` med följande template:

```python
#!/usr/bin/env python3
"""
MCP Server för [beskriv vad din server gör].
"""

import sys
import asyncio
from pathlib import Path

# Lägg till parent directory för att importera mcp_common
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.server import Server
import mcp.types as types
from mcp_common import (
    create_text_response,
    create_error_response,
    run_mcp_server,
    safe_get_arg,
    MCPToolBuilder
)

# Skapa server-instans
server = Server("min-server-namn")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """Lista tillgängliga verktyg."""
    return [
        MCPToolBuilder.create_tool(
            name="mitt_verktyg",
            description="Beskriv vad verktyget gör",
            properties={
                "parameter1": {
                    "type": "string",
                    "description": "Beskrivning av parameter1"
                },
                "parameter2": {
                    "type": "number",
                    "description": "Beskrivning av parameter2",
                    "default": 10
                }
            },
            required=["parameter1"]  # Endast obligatoriska parametrar
        ),
        # Lägg till fler verktyg här...
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Hantera verktygsanrop."""

    if name == "mitt_verktyg":
        # Hämta parametrar säkert
        param1 = safe_get_arg(arguments, "parameter1")
        param2 = safe_get_arg(arguments, "parameter2", 10)  # default = 10

        # Validera input
        if not param1:
            return create_error_response("parameter1 är obligatorisk")

        try:
            # Din logik här
            resultat = f"Utförde operation med {param1} och {param2}"

            # Returnera framgång
            return create_text_response(resultat)

        except Exception as e:
            # Returnera fel
            return create_error_response(f"Något gick fel: {str(e)}")

    else:
        raise ValueError(f"Okänt verktyg: {name}")


async def main():
    """Huvudingång för MCP-servern."""
    await run_mcp_server(
        server,
        "min-server-namn",  # Servernamn
        "0.1.0"             # Version
    )


if __name__ == "__main__":
    asyncio.run(main())
```

### Steg 3: Gör filen körbar

```bash
chmod +x min_server.py
```

### Steg 4: Lägg till i Claude Desktop konfiguration

Redigera `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "min-nya-server": {
      "command": "python3",
      "args": [
        "/Users/spjutbjorn/git/pythonTools/mcp/min-nya-server/min_server.py"
      ]
    }
  }
}
```

### Steg 5: Starta om Claude Desktop

Servern är nu tillgänglig i Claude!

## Detaljerad Guide

### 1. Import-mönster

Använd alltid detta import-mönster för att hitta `mcp_common.py`:

```python
import sys
from pathlib import Path

# Lägg till parent directory till Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_common import create_text_response, ...
```

### 2. Skapa verktyg med MCPToolBuilder

#### Enkelt verktyg utan parametrar

```python
MCPToolBuilder.create_tool(
    name="hello",
    description="Säg hej",
    properties={},
    required=[]
)
```

#### Verktyg med parametrar

```python
MCPToolBuilder.create_tool(
    name="calculate",
    description="Utför en beräkning",
    properties={
        "operation": {
            "type": "string",
            "description": "Operation: add, subtract, multiply, divide",
            "enum": ["add", "subtract", "multiply", "divide"]
        },
        "a": {
            "type": "number",
            "description": "Första talet"
        },
        "b": {
            "type": "number",
            "description": "Andra talet"
        }
    },
    required=["operation", "a", "b"]
)
```

#### Verktyg med valfria parametrar

```python
MCPToolBuilder.create_tool(
    name="search",
    description="Sök efter något",
    properties={
        "query": {
            "type": "string",
            "description": "Sökfråga"
        },
        "limit": {
            "type": "number",
            "description": "Max antal resultat",
            "default": 10
        },
        "filter": {
            "type": "string",
            "description": "Valfritt filter"
        }
    },
    required=["query"]  # Endast query är obligatorisk
)
```

#### Verktyg med array-parametrar

```python
MCPToolBuilder.create_tool(
    name="process_items",
    description="Bearbeta en lista av items",
    properties={
        "items": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Lista av items att bearbeta"
        },
        "options": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Valfria alternativ"
        }
    },
    required=["items"]
)
```

### 3. Hantera verktygsanrop

#### Grundläggande mönster

```python
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None):
    if name == "mitt_verktyg":
        # Hämta parametrar
        param = safe_get_arg(arguments, "param", "default_value")

        # Din logik
        result = do_something(param)

        # Returnera resultat
        return create_text_response(result)

    elif name == "annat_verktyg":
        # ... hantera annat verktyg
        pass

    else:
        raise ValueError(f"Okänt verktyg: {name}")
```

#### Felhantering

```python
if name == "mitt_verktyg":
    param = safe_get_arg(arguments, "param")

    # Validering
    if not param:
        return create_error_response("param är obligatorisk")

    if not isinstance(param, str):
        return create_error_response("param måste vara en sträng")

    try:
        result = risky_operation(param)
        return create_text_response(f"Framgång: {result}")
    except FileNotFoundError:
        return create_error_response("Filen hittades inte")
    except PermissionError:
        return create_error_response("Åtkomst nekad")
    except Exception as e:
        return create_error_response(f"Oväntat fel: {str(e)}")
```

#### Formaterade svar

```python
# Enkelt svar
return create_text_response("Operation lyckades!")

# Flerlinje-svar
result = f"""
Operation slutförd!

Resultat:
- Bearbetade objekt: {count}
- Tid: {elapsed}s
- Status: Framgång

Detaljer: {details}
"""
return create_text_response(result.strip())

# Tabell-format
result = "Resultat:\n\n"
result += f"{'Namn':<20} {'Värde':<10} {'Status'}\n"
result += "=" * 50 + "\n"
for item in items:
    result += f"{item.name:<20} {item.value:<10} {item.status}\n"
return create_text_response(result)
```

### 4. Avancerade mönster

#### Server med persistent state

```python
import json
from pathlib import Path

# Global state
STATE_FILE = Path(__file__).parent / "state.json"
state = {"items": []}

def load_state():
    """Ladda state från fil."""
    global state
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)

def save_state():
    """Spara state till fil."""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

# Ladda state vid start
load_state()

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None):
    if name == "add_item":
        item = safe_get_arg(arguments, "item")
        state["items"].append(item)
        save_state()
        return create_text_response(f"Lade till: {item}")
```

#### Server med background thread

```python
import threading

def background_task():
    """Bakgrundsuppgift som körs kontinuerligt."""
    while True:
        # Gör något
        time.sleep(10)

async def main():
    # Starta bakgrundsuppgift
    bg_thread = threading.Thread(target=background_task, daemon=True)
    bg_thread.start()

    # Starta MCP-server
    await run_mcp_server(server, "min-server", "0.1.0")
```

#### Server med HTTP-server (som word-cloud)

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

def run_http_server():
    """Kör HTTP-server i bakgrunden."""
    httpd = HTTPServer(('localhost', 8080), MyHTTPHandler)
    print("HTTP server på http://localhost:8080/")
    httpd.serve_forever()

async def main():
    # Starta HTTP-server
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    http_thread.start()

    # Starta MCP-server
    await run_mcp_server(server, "min-server", "0.1.0")
```

## Best Practices

### 1. Namngivning

- **Server namn**: lowercase-with-dashes (t.ex. "word-cloud", "large-files-manager")
- **Verktygsnamn**: lowercase_with_underscores (t.ex. "add_word", "list_files")
- **Parametrar**: lowercase_with_underscores (t.ex. "file_path", "max_size")

### 2. Beskrivningar

Skriv tydliga beskrivningar:

```python
# BRA
MCPToolBuilder.create_tool(
    name="search_files",
    description="Search for files by name pattern in a directory tree",
    ...
)

# DÅLIGT
MCPToolBuilder.create_tool(
    name="search_files",
    description="Search",
    ...
)
```

### 3. Validering

Validera alltid input:

```python
# Validera obligatoriska parametrar
if not param:
    return create_error_response("param är obligatorisk")

# Validera typer
if not isinstance(param, str):
    return create_error_response("param måste vara en sträng")

# Validera värden
if param not in ["option1", "option2"]:
    return create_error_response("param måste vara 'option1' eller 'option2'")

# Validera intervall
if not (1 <= param <= 10):
    return create_error_response("param måste vara mellan 1 och 10")
```

### 4. Felhantering

Fånga specifika fel:

```python
try:
    result = do_something()
    return create_text_response(result)
except FileNotFoundError as e:
    return create_error_response(f"Fil hittades inte: {e.filename}")
except PermissionError:
    return create_error_response("Åtkomst nekad")
except ValueError as e:
    return create_error_response(f"Ogiltigt värde: {str(e)}")
except Exception as e:
    return create_error_response(f"Oväntat fel: {str(e)}")
```

### 5. Dokumentation

Skapa alltid en README.md:

```markdown
# Min Server

Beskrivning av vad servern gör.

## Verktyg

- `verktyg1` - Beskrivning
- `verktyg2` - Beskrivning

## Installation

...

## Användning

...

## Exempel

...
```

## Komplett Exempel: Calculator Server

```python
#!/usr/bin/env python3
"""
MCP Server för grundläggande matematiska operationer.
"""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.server import Server
import mcp.types as types
from mcp_common import (
    create_text_response,
    create_error_response,
    run_mcp_server,
    safe_get_arg,
    MCPToolBuilder
)

server = Server("calculator")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """Lista tillgängliga verktyg."""
    return [
        MCPToolBuilder.create_tool(
            name="calculate",
            description="Perform basic mathematical operations",
            properties={
                "operation": {
                    "type": "string",
                    "description": "Mathematical operation",
                    "enum": ["add", "subtract", "multiply", "divide", "power"]
                },
                "a": {
                    "type": "number",
                    "description": "First number"
                },
                "b": {
                    "type": "number",
                    "description": "Second number"
                }
            },
            required=["operation", "a", "b"]
        ),
        MCPToolBuilder.create_tool(
            name="convert",
            description="Convert between units",
            properties={
                "value": {
                    "type": "number",
                    "description": "Value to convert"
                },
                "from_unit": {
                    "type": "string",
                    "description": "Source unit (celsius, fahrenheit, km, miles)"
                },
                "to_unit": {
                    "type": "string",
                    "description": "Target unit"
                }
            },
            required=["value", "from_unit", "to_unit"]
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Hantera verktygsanrop."""

    if name == "calculate":
        operation = safe_get_arg(arguments, "operation")
        a = safe_get_arg(arguments, "a")
        b = safe_get_arg(arguments, "b")

        # Validera
        if operation not in ["add", "subtract", "multiply", "divide", "power"]:
            return create_error_response("Ogiltig operation")

        if a is None or b is None:
            return create_error_response("Båda talen måste anges")

        try:
            # Utför operation
            if operation == "add":
                result = a + b
            elif operation == "subtract":
                result = a - b
            elif operation == "multiply":
                result = a * b
            elif operation == "divide":
                if b == 0:
                    return create_error_response("Division med noll är inte tillåtet")
                result = a / b
            elif operation == "power":
                result = a ** b

            return create_text_response(
                f"{a} {operation} {b} = {result}"
            )

        except Exception as e:
            return create_error_response(f"Beräkningsfel: {str(e)}")

    elif name == "convert":
        value = safe_get_arg(arguments, "value")
        from_unit = safe_get_arg(arguments, "from_unit", "").lower()
        to_unit = safe_get_arg(arguments, "to_unit", "").lower()

        try:
            # Temperatur
            if from_unit == "celsius" and to_unit == "fahrenheit":
                result = (value * 9/5) + 32
            elif from_unit == "fahrenheit" and to_unit == "celsius":
                result = (value - 32) * 5/9
            # Distans
            elif from_unit == "km" and to_unit == "miles":
                result = value * 0.621371
            elif from_unit == "miles" and to_unit == "km":
                result = value * 1.60934
            else:
                return create_error_response(
                    f"Konvertering från {from_unit} till {to_unit} stöds inte"
                )

            return create_text_response(
                f"{value} {from_unit} = {result:.2f} {to_unit}"
            )

        except Exception as e:
            return create_error_response(f"Konverteringsfel: {str(e)}")

    else:
        raise ValueError(f"Okänt verktyg: {name}")


async def main():
    """Huvudingång för MCP-servern."""
    await run_mcp_server(server, "calculator", "0.1.0")


if __name__ == "__main__":
    asyncio.run(main())
```

## Felsökning

### ImportError: No module named 'mcp_common'

Kontrollera att:
1. `mcp_common.py` finns i parent-foldern
2. Du använder rätt sys.path.insert:
   ```python
   sys.path.insert(0, str(Path(__file__).parent.parent))
   ```

### Server dyker inte upp i Claude

1. Kontrollera konfigurationen i `claude_desktop_config.json`
2. Verifiera att sökvägen är korrekt
3. Starta om Claude Desktop
4. Kolla efter fel i Claude Desktop logs

### Verktyg fungerar inte

1. Kontrollera att verktygsnamnet stämmer mellan `list_tools()` och `call_tool()`
2. Validera att alla required parametrar skickas
3. Kontrollera att du returnerar rätt typ (`list[types.TextContent]`)

## Nästa steg

1. Studera befintliga servrar i `large-files-manager/` och `word-cloud/`
2. Kopiera template-koden ovan
3. Anpassa för ditt användningsfall
4. Testa lokalt innan du lägger till i Claude Desktop
5. Skriv dokumentation i README.md

## Resurser

- [MCP Documentation](https://modelcontextprotocol.io/)
- Exempel: `large-files-manager/large_files_mcp_server.py`
- Exempel: `word-cloud/word_cloud_server.py`
- Common utilities: `mcp_common.py`

---

Lycka till med din MCP-server! 🚀
