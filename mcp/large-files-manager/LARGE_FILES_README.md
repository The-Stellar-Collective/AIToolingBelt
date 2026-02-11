# Large Files MCP Server

En MCP (Model Context Protocol) server i Python för att hitta och hantera stora filer på din disk.

## Funktioner

- **list_large_files**: Hitta och lista de största filerna på disken i en toplista
- **delete_file**: Ta bort specifika filer (med säkerhetsbekräftelse)
- **get_file_info**: Få detaljerad information om en specifik fil

## Installation

1. Installera Python 3.10 eller senare

2. Installera dependencies:
```bash
pip install -r requirements_large_files.txt
```

## Konfiguration i Claude Desktop

För att använda denna MCP-server med Claude Desktop, lägg till följande i din MCP-konfigurationsfil:

### macOS
Redigera: `~/Library/Application Support/Claude/claude_desktop_config.json`

### Windows
Redigera: `%APPDATA%\Claude\claude_desktop_config.json`

### Konfiguration:
```json
{
  "mcpServers": {
    "large-files-manager": {
      "command": "python3",
      "args": [
        "/Users/spjutbjorn/git/pythonTools/large_files_mcp_server.py"
      ]
    }
  }
}
```

**Obs**: Uppdatera sökvägen till att matcha var du har sparat `large_files_mcp_server.py`

## Användning

När servern är konfigurerad kan du använda följande kommandon i Claude:

### Hitta stora filer

```
Använd list_large_files för att hitta de 20 största filerna i min hemkatalog
```

Parametrar:
- `start_path`: Rotkatalog att börja söka från (default: `~`)
- `top_n`: Antal filer att returnera (default: 20)
- `min_size_mb`: Minsta filstorlek i MB (default: 1.0)
- `exclude_dirs`: Lista med katalognamn att exkludera

### Ta bort en fil

```
Använd delete_file för att ta bort /path/to/large/file.txt
```

**VARNING**: Detta tar bort filen permanent! Du måste sätta `confirm: true` för att bekräfta borttagningen.

### Få filinformation

```
Använd get_file_info för att få information om /path/to/file.txt
```

## Exempel

### Hitta stora filer i hemkatalogen
```
list_large_files med start_path: "~", top_n: 30, min_size_mb: 100
```

### Hitta stora videofiler
```
list_large_files med start_path: "~/Movies", top_n: 10, min_size_mb: 500
```

### Ta bort en specifik fil
```
delete_file med file_path: "/Users/username/large_video.mp4", confirm: true
```

## Säkerhetsfunktioner

- Servern hoppar automatiskt över vanliga systemkataloger (`.git`, `node_modules`, `Library`, `Applications`, `System`)
- Borttagning av filer kräver explicit bekräftelse med `confirm: true`
- Servern hanterar behörighetsfel och otillgängliga filer graciöst
- Symboliska länkar ignoreras för att undvika problem

## Tekniska detaljer

- Bygger på MCP (Model Context Protocol) SDK
- Använder `os.walk()` för att traversera filsystemet
- Sorterar filer efter storlek i fallande ordning
- Visar filstorlekar i läsbart format (B, KB, MB, GB, TB)

## Felsökning

Om servern inte dyker upp i Claude:
1. Kontrollera att sökvägen i konfigurationsfilen är korrekt
2. Verifiera att Python 3.10+ är installerat: `python3 --version`
3. Kontrollera att MCP-paketet är installerat: `pip list | grep mcp`
4. Starta om Claude Desktop efter att ha uppdaterat konfigurationen

## Licens

Open source - använd fritt!
