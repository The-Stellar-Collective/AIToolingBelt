# MCP Servers Collection

En samling av MCP (Model Context Protocol) servrar för att utöka Claude Desktop med kraftfulla verktyg.

## 🚀 Snabbstart

### Första gången?

**Enklaste sättet - Kör ett kommando:**

```bash
python3 install.py
```

Eller **säg till din AI:** *"Läs in och installera det som står i SETUP.md"*

**Vad händer:**
- 🔍 Detekterar automatiskt ditt OS (Mac/Windows/Linux)
- ✅ Kontrollerar Python och pip
- 📦 Installerar alla dependencies
- ⚙️ Konfigurerar Claude Desktop
- ✓ Verifierar installationen

📚 **Guider:**
- **[install.py](install.py)** - 🤖 Automatiskt installations-script (kör detta!)
- **[SETUP.md](SETUP.md)** - Steg-för-steg guide och AI-instruktioner
- **[PYTHON_INSTALL.md](PYTHON_INSTALL.md)** - Installera Python på Mac/Windows
- **[INIT.md](INIT.md)** - Skapa din egen MCP-server

## Struktur

```
mcp/
├── install.py                 # 🤖 Automatiskt installations-script (börja här!)
├── verify_installation.py     # Verifierings-script för installation
├── mcp_common.py              # Delade utilities för alla MCP-servrar
├── SETUP.md                   # Installations-guide och AI-instruktioner
├── PYTHON_INSTALL.md          # Python installationsguide för Mac/Windows
├── INIT.md                    # Guide för att skapa nya MCP-servrar
├── README.md                  # Denna fil
├── large-files-manager/       # Hitta och hantera stora filer
│   ├── large_files_mcp_server.py
│   ├── requirements_large_files.txt
│   └── LARGE_FILES_README.md
└── word-cloud/                # Live word cloud visualisering
    ├── word_cloud_server.py
    ├── index.html
    ├── words.json (genereras automatiskt)
    └── README.md
```

## Tillgängliga Servrar

### 1. Large Files Manager
Hitta de största filerna på din disk och ta bort dem.

**Verktyg:**
- `list_large_files` - Lista största filerna
- `delete_file` - Ta bort en fil (med bekräftelse)
- `get_file_info` - Få information om en fil

**Dokumentation:** [large-files-manager/LARGE_FILES_README.md](large-files-manager/LARGE_FILES_README.md)

### 2. Word Cloud Manager
Skapa ett live-uppdaterat ordmoln som visas i webbläsaren med automatisk kategorisering!

**Verktyg:**
- `add_word` - Lägg till ord med automatisk kategorisering (9 kategorier: MCP, verktyg, språk, ramverk, etc.)
- `add_mcp_servers` - 🚀 Lägg till alla installerade MCP-servrar automatiskt!
- `remove_word` - Ta bort ett ord
- `clear_cloud` - Rensa alla ord
- `list_words` - Lista alla ord
- `list_categories` - Visa alla tillgängliga kategorier
- `list_by_category` - Lista ord grupperade efter kategori
- `open_browser` - Öppna ordmolnet automatiskt i din webbläsare

**Features:**
- 🚀 Auto-import av alla installerade MCP-servrar
- 🎨 Automatisk kategorisering baserat på nyckelord
- 📊 Interaktivt D3.js ordmoln med smooth animationer
- 🌈 Färgkodning per kategori (MCP-servrar i rött!)
- ⚡ Live-uppdateringar i realtid via SSE
- 💎 Modern glassmorphism design med dark mode
- 🖱️ Hover-tooltips med kategori och beskrivning
- 📱 Responsiv layout

**Webbgränssnitt:** http://localhost:8765/ (öppnas automatiskt med `open_browser`)

**Dokumentation:** [word-cloud/README.md](word-cloud/README.md)

## Installation

### Automatisk Installation (Rekommenderat)

**Kör installations-scriptet:**

```bash
python3 install.py
```

**eller säg till din AI:**
```
Kör install.py för att installera allt automatiskt
```

Detta script:
- Detekterar ditt OS automatiskt
- Kontrollerar Python-version
- Installerar alla dependencies
- Konfigurerar Claude Desktop
- Verifierar installationen

### Manuell Installation

Om du behöver installera manuellt, se [SETUP.md](SETUP.md) för steg-för-steg instruktioner.

**Har du inte Python installerat?**

📖 **Se [PYTHON_INSTALL.md](PYTHON_INSTALL.md)** för detaljerade instruktioner för Mac och Windows.

3. Konfigurera Claude Desktop

Redigera: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "large-files-manager": {
      "command": "python3",
      "args": [
        "/Users/spjutbjorn/git/pythonTools/mcp/large-files-manager/large_files_mcp_server.py"
      ]
    },
    "word-cloud": {
      "command": "python3",
      "args": [
        "/Users/spjutbjorn/git/pythonTools/mcp/word-cloud/word_cloud_server.py"
      ]
    }
  }
}
```

4. Starta om Claude Desktop

5. **Verifiera installationen:**
```bash
python3 verify_installation.py
```

**Instruktion till AI:**
```
Kör verifierings-scriptet för att kontrollera installationen
```

## Gemensamma Komponenter (mcp_common.py)

Alla servrar använder gemensamma utilities från `mcp_common.py`:

- `create_text_response()` - Skapa standardiserade textsvar
- `create_error_response()` - Skapa standardiserade felsvar
- `run_mcp_server()` - Kör en MCP-server med standardkonfiguration
- `safe_get_arg()` - Säker argumenthämtning
- `MCPToolBuilder` - Hjälpklass för att bygga verktyg

## Användningsexempel

### Large Files Manager
```
Hitta de 30 största filerna i min hemkatalog som är större än 100 MB
```

### Word Cloud
```
Öppna ordmolnet i webbläsaren

Lägg till alla MCP-servrar
Lägg till ordet "Python" med storlek 8
Lägg till ordet "Docker" med storlek 7
Lägg till ordet "React" med storlek 9

Lista ord efter kategori
```

**Resultat:**
```
📁 MCP Server (2 ord)
  • large-files-manager (size: 7)
  • word-cloud (size: 7)

📁 Verktyg (1 ord)
  • Docker (size: 7)

📁 Programmeringsspråk (1 ord)
  • Python (size: 8)

📁 Ramverk (1 ord)
  • React (size: 9)
```

- MCP-servrar läggs till automatiskt från config
- Orden kategoriseras automatiskt
- Färgkodning (MCP-servrar i rött!)
- Live-uppdatering i webbläsaren!

## Skapa Din Egen MCP-Server

📖 **Se [INIT.md](INIT.md)** för en komplett guide med templates, exempel och best practices!

### Snabbstart

1. **Skapa en ny folder i `mcp/`**
   ```bash
   mkdir mcp/min-nya-server
   ```

2. **Kopiera template från INIT.md** eller använd detta minimala exempel:

```python
#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.server import Server
import mcp.types as types
from mcp_common import create_text_response, run_mcp_server, MCPToolBuilder

server = Server("my-server-name")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        MCPToolBuilder.create_tool(
            name="my_tool",
            description="What my tool does",
            properties={
                "param": {
                    "type": "string",
                    "description": "Parameter description"
                }
            },
            required=["param"]
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None):
    if name == "my_tool":
        return create_text_response("Success!")

async def main():
    await run_mcp_server(server, "my-server-name", "0.1.0")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

3. **Lägg till i Claude Desktop konfiguration**
4. **Starta om Claude Desktop**

**För mer avancerade exempel, templates och best practices - se [INIT.md](INIT.md)**

## Felsökning

**Servern dyker inte upp i Claude:**
- Kontrollera att sökvägen i konfigurationsfilen är korrekt
- Verifiera Python-versionen: `python3 --version`
- Kontrollera att MCP är installerat: `pip3 list | grep mcp`
- Starta om Claude Desktop

**Import-fel:**
- Kontrollera att `mcp_common.py` finns i mcp-roten
- Verifiera att sys.path.insert används korrekt

**Port-konflikter (word-cloud):**
- Kontrollera att port 8765 inte används: `lsof -i :8765`
- Ändra SERVER_PORT i word_cloud_server.py vid behov

## Dokumentation

### Kom igång
- **[install.py](install.py)** - 🤖 Automatiskt installations-script (KÖR DETTA FÖRST!)
- **[verify_installation.py](verify_installation.py)** - Verifierings-script
- **[SETUP.md](SETUP.md)** - Installations-guide och AI-instruktioner
- **[README.md](README.md)** - Översikt och snabbstart

### Installation & Utveckling
- **[PYTHON_INSTALL.md](PYTHON_INSTALL.md)** - Python installationsguide för Mac/Windows
- **[INIT.md](INIT.md)** - Komplett guide för att skapa nya MCP-servrar
- **[mcp_common.py](mcp_common.py)** - Återanvändbara komponenter och utilities

### Server-dokumentation
- **[large-files-manager/LARGE_FILES_README.md](large-files-manager/LARGE_FILES_README.md)** - Large Files Manager
- **[word-cloud/README.md](word-cloud/README.md)** - Word Cloud Manager

## Resurser

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Python Official Documentation](https://docs.python.org/)
- [Claude Desktop](https://claude.ai/download)

## Licens

Open source - använd fritt!
