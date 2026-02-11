# Live Word Cloud MCP Server

En MCP-server som skapar ett live-uppdaterat ordmoln som visas i webbläsaren. Lägg till ord via Claude Chat och se dem dyka upp i realtid!

## Funktioner

- **add_word**: Lägg till ett ord till ordmolnet med beskrivning och storlek (automatisk kategorisering!)
- **add_mcp_servers**: Lägg till alla installerade MCP-servrar från Claude Desktop config automatiskt! 🚀
- **remove_word**: Ta bort ett ord från ordmolnet
- **clear_cloud**: Rensa alla ord
- **list_words**: Lista alla ord i molnet
- **list_categories**: Visa alla tillgängliga kategorier och deras beskrivningar
- **list_by_category**: Lista ord grupperade efter kategori i strukturerad form
- **open_browser**: Öppna ordmolnet automatiskt i din standard-webbläsare

## Installation

1. Installera Python 3.10 eller senare

2. Requirements är redan installerade (används från parent mcp folder)

## Konfiguration

Lägg till i `~/Library/Application Support/Claude/claude_desktop_config.json`:

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

## Användning

1. Starta om Claude Desktop efter konfiguration

2. Öppna webbgränssnittet automatiskt:
   ```
   Öppna ordmolnet i webbläsaren
   ```
   eller
   ```
   Använd open_browser
   ```

   Detta öppnar automatiskt http://localhost:8765/ i din standard-webbläsare!

   Du kan också öppna URL:en manuellt: http://localhost:8765/

3. Lägg till ord via Claude:
   ```
   Lägg till ordet "Python" med beskrivning "språk" och storlek 8
   ```

4. **Interagera med ordmolnet:**
   - **Hover över ord** för att se detaljer i tooltip
   - **Ordstorlek** visar betydelse (1-10)
   - **Färg** indikerar kategori
   - **Live-uppdatering** när nya ord läggs till
   - **Smooth animationer** för alla ändringar

5. Se ordmolnet uppdateras i realtid!

## Exempel

### Lägg till alla MCP-servrar automatiskt! 🚀
```
Lägg till alla MCP-servrar
```
eller
```
Använd add_mcp_servers
```

Detta läser automatiskt din Claude Desktop config och lägger till alla installerade MCP-servrar i ordmolnet!

**Resultat:**
```
✓ Lade till MCP-servrar i ordmolnet!

Nya servrar (2):
  • large-files-manager
  • word-cloud

Totalt ord i molnet: 2
```

### Öppna ordmolnet i webbläsaren
```
Öppna ordmolnet
```
eller
```
Använd open_browser
```
Ordmolnet öppnas automatiskt i din standard-webbläsare!

### Visa tillgängliga kategorier
```
Visa alla kategorier
```
eller
```
Använd list_categories
```

### Lägg till ord (automatisk kategorisering)
```
Lägg till ordet "Docker" med storlek 8
Lägg till ordet "Python" med storlek 9
Lägg till ordet "React" med storlek 7
```
Orden kategoriseras automatiskt baserat på nyckelord!

### Lägg till ord med manuell kategori
```
add_word: word="MyTool", description="verktyg", size=7
add_word: word="Kubernetes", description="teknologi", size=9
add_word: word="Microservices", description="koncept", size=6
```

### Lista ord grupperat efter kategori
```
Lista ord efter kategori
```
eller
```
Använd list_by_category
```

### Lista alla ord
```
list_words
```

### Ta bort ord
```
remove_word: word="Docker"
```

### Rensa alla ord
```
clear_cloud: confirm=true
```

## Automatisk Kategorisering

Ord kategoriseras automatiskt baserat på nyckelord! Du kan också ange kategori manuellt i beskrivningen.

### Tillgängliga Kategorier

| Kategori | Beskrivning | Färg | Exempel |
|----------|-------------|------|---------|
| **MCP Server** | Installerade MCP-servrar | Röd | large-files-manager, word-cloud |
| **Verktyg** | Programvaruverktyg och applikationer | Lila | Docker, Git, VSCode, Jenkins |
| **Språk** | Programmeringsspråk | Grön | Python, JavaScript, Java, Go |
| **Ramverk** | Ramverk och bibliotek | Rosa/Gul | React, Django, Spring, Express |
| **Teknologi** | Plattformar och teknologier | Rosa/Röd | Kubernetes, AWS, Cloud |
| **Koncept** | Koncept och metodik | Blå | Agile, DevOps, CI/CD, REST |
| **Databas** | Databaser och datalagring | Turkos/Lila | PostgreSQL, MongoDB, Redis |
| **Roll** | Roller och titlar | Pastellblå | Developer, Architect, Engineer |
| **Metod** | Metoder och processer | Lila/Blå | Scrum, Kanban, Lean |

### Hur kategoriseringen fungerar

1. **Automatisk**: Systemet känner igen ord som "Docker" → Verktyg, "Python" → Språk
2. **Manuell**: Sätt `description="verktyg"` för att tvinga en kategori
3. **Visuell gruppering**: Ordmolnet visar ord grupperade efter kategori med headers

## Tekniska detaljer

- **Webbserver** på port 8765
- **Live-uppdateringar** via Server-Sent Events (SSE)
- **Data lagras** i `words.json`
- **Visualisering** med D3.js och d3-cloud för interaktivt ordmoln
- **Glassmorphism design** med dark mode och gradient-bakgrund
- **Animerade övergångar** för smooth uppdateringar
- **Hover-tooltips** med kategori och beskrivning
- **Kategorifärger** för varje typ av ord (MCP i rött, Verktyg i lila, etc.)
- **Responsiv layout** som anpassar sig till fönsterstorlek

## Felsökning

Om servern inte startar:
1. Kontrollera att port 8765 inte används: `lsof -i :8765`
2. Verifiera att mcp_common.py finns i parent-mappen
3. Starta om Claude Desktop
4. Kolla console för felmeddelanden
