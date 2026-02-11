# MCP Setup - Automatisk Installation

> **Säg till din AI: "Läs in och installera det som står i SETUP.md"**

Denna fil innehåller alla kommandon och steg för att automatiskt sätta upp MCP-servrar.

---

## 🤖 ENKLASTE METODEN - Automatiskt Installations-Script

**Kör detta kommando för fullautomatisk installation:**

```bash
python3 /Users/spjutbjorn/git/pythonTools/mcp/install.py
```

**Detta script gör allt automatiskt:**
- ✓ Detekterar ditt OS (macOS/Windows/Linux)
- ✓ Kontrollerar Python-version
- ✓ Installerar pip om det saknas
- ✓ Installerar MCP och alla dependencies
- ✓ Gör server-filer körbara
- ✓ Konfigurerar Claude Desktop automatiskt
- ✓ Verifierar installationen

**AI-instruktion:**
```
Kör install.py scriptet för att installera allt automatiskt
```

**Efter att scriptet är klart:**
1. Starta om Claude Desktop
2. Testa servrarna enligt instruktionerna

---

## 📋 MANUELL INSTALLATION (om install.py inte fungerar)

Om du föredrar manuell installation eller om install.py inte fungerar, följ dessa steg:

### 🚀 AUTOMATISK INSTALLATION - KÖR DESSA STEG

### STEG 1: Verifiera Python Installation

```bash
# Kontrollera Python version
python3 --version || python --version
```

**Förväntat resultat:** Python 3.10 eller senare

**Om Python saknas:**
- macOS: `brew install python3`
- Windows (PowerShell): `winget install Python.Python.3.11`
- Eller se: PYTHON_INSTALL.md

---

### STEG 2: Verifiera pip Installation

```bash
# Kontrollera pip version
pip3 --version || pip --version
```

**Förväntat resultat:** pip 23.x eller senare

**Om pip saknas:**
```bash
# macOS/Linux
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py

# Windows
python -m ensurepip --upgrade
```

---

### STEG 3: Installera MCP Dependencies

```bash
# Navigera till mcp folder
cd /Users/spjutbjorn/git/pythonTools/mcp/large-files-manager

# Installera requirements
pip3 install -r requirements_large_files.txt
```

**Alternativ (global installation):**
```bash
pip3 install mcp>=1.0.0
```

---

### STEG 4: Verifiera MCP Installation

```bash
# Testa import
python3 -c "import mcp; print('MCP installed successfully')"

# Verifiera mcp_common.py
python3 -c "import sys; sys.path.insert(0, '/Users/spjutbjorn/git/pythonTools/mcp'); from mcp_common import create_text_response; print('mcp_common.py works')"
```

**Förväntat resultat:** Inga fel, success-meddelanden

---

### STEG 5: Gör serverfiler körbara

```bash
# Gör MCP-servrar körbara
chmod +x /Users/spjutbjorn/git/pythonTools/mcp/large-files-manager/large_files_mcp_server.py
chmod +x /Users/spjutbjorn/git/pythonTools/mcp/word-cloud/word_cloud_server.py
```

---

### STEG 6: Konfigurera Claude Desktop

**Fil att redigera:**
```
macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
Windows: %APPDATA%\Claude\claude_desktop_config.json
```

**Innehåll (ersätt hela filen eller lägg till i mcpServers):**

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

**Kommando för att öppna filen:**
```bash
# macOS
open ~/Library/Application\ Support/Claude/claude_desktop_config.json

# eller redigera direkt via kod (se nedan)
```

---

### STEG 7: Testa MCP-servrar (Valfritt)

```bash
# Testa large-files-manager
timeout 5 python3 /Users/spjutbjorn/git/pythonTools/mcp/large-files-manager/large_files_mcp_server.py &

# Testa word-cloud
timeout 5 python3 /Users/spjutbjorn/git/pythonTools/mcp/word-cloud/word_cloud_server.py &

# Om inga fel visas är servrarna OK
# Tryck Ctrl+C för att avbryta
```

---

### STEG 8: Starta om Claude Desktop

**macOS:**
```bash
# Avsluta Claude Desktop
killall Claude 2>/dev/null || true

# Öppna igen
open -a Claude
```

**Windows (PowerShell):**
```powershell
# Avsluta Claude Desktop
Stop-Process -Name "Claude" -ErrorAction SilentlyContinue

# Öppna igen (justera sökväg om nödvändigt)
Start-Process "C:\Users\$env:USERNAME\AppData\Local\AnthropicClaude\Claude.exe"
```

---

## ✅ VERIFIERING

### Automatisk Verifiering (Rekommenderat)

**Kör verifierings-scriptet:**

```bash
python3 /Users/spjutbjorn/git/pythonTools/mcp/verify_installation.py
```

Detta script kontrollerar:
- ✓ Python version
- ✓ MCP paket installation
- ✓ mcp_common.py
- ✓ Server-filer
- ✓ Claude Desktop konfiguration
- ✓ Alla dependencies

**Förväntat resultat:** 🎉 All checks passed!

---

### Manuell Verifiering

Efter omstart av Claude Desktop, verifiera att servrarna fungerar:

### 1. Large Files Manager

**Testa i Claude:**
```
Använd list_large_files för att hitta de 10 största filerna i min hemkatalog
```

**Förväntat resultat:** Lista med stora filer

### 2. Word Cloud Manager

**Testa i Claude:**
```
Använd add_word för att lägga till ordet "Test" med beskrivning "demo" och storlek 5
```

**Sedan öppna:**
```
http://localhost:8765/
```

**Förväntat resultat:** Ordet "Test" visas i ordmolnet

---

## 🔧 FELSÖKNING

### Problem: Python inte hittat

```bash
# macOS - Installera via Homebrew
brew install python3

# Windows - Installera via winget
winget install Python.Python.3.11
```

### Problem: pip inte hittat

```bash
# Installera pip
python3 -m ensurepip --upgrade
```

### Problem: MCP installation misslyckades

```bash
# Uppgradera pip först
pip3 install --upgrade pip

# Försök igen
pip3 install mcp>=1.0.0
```

### Problem: Permission denied

```bash
# macOS/Linux - Använd --user flag
pip3 install --user mcp

# Eller använd sudo (inte rekommenderat)
sudo pip3 install mcp
```

### Problem: Claude Desktop konfiguration

```bash
# Verifiera att filen finns
ls -la ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Kontrollera innehåll
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Validera JSON syntax
python3 -m json.tool ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### Problem: Servrar dyker inte upp i Claude

1. Kontrollera att Python-sökvägarna är korrekta
2. Verifiera att `.py` filerna är körbara: `ls -l *.py`
3. Starta om Claude Desktop helt
4. Kontrollera Claude Desktop logs

---

## 📋 KOMMANDO-SAMMANFATTNING (Kopiera och kör alla)

### macOS - Komplett installation

```bash
# Verifiera Python
python3 --version

# Installera MCP
cd /Users/spjutbjorn/git/pythonTools/mcp/large-files-manager
pip3 install -r requirements_large_files.txt

# Gör filer körbara
chmod +x /Users/spjutbjorn/git/pythonTools/mcp/large-files-manager/large_files_mcp_server.py
chmod +x /Users/spjutbjorn/git/pythonTools/mcp/word-cloud/word_cloud_server.py

# Verifiera
python3 -c "import mcp; print('✓ MCP installed')"

echo "✓ Installation klar! Konfigurera nu Claude Desktop och starta om."
```

### Windows - Komplett installation (PowerShell)

```powershell
# Verifiera Python
python --version

# Installera MCP
cd C:\Users\$env:USERNAME\git\pythonTools\mcp\large-files-manager
pip install -r requirements_large_files.txt

# Verifiera
python -c "import mcp; print('✓ MCP installed')"

Write-Host "✓ Installation klar! Konfigurera nu Claude Desktop och starta om."
```

---

## 🎯 AI-INSTRUKTIONER

**För AI-assistenter: När användaren säger "läs in och installera det som står i SETUP.md", utför följande:**

1. **Identifiera operativsystem** (macOS eller Windows)

2. **Kör verifieringskommandon:**
   - Kontrollera Python version
   - Kontrollera pip version

3. **Installera dependencies:**
   - Kör pip install kommando
   - Verifiera installation

4. **Gör filer körbara** (endast macOS/Linux):
   - chmod +x på båda server-filerna

5. **Uppdatera Claude Desktop konfiguration:**
   - Läs befintlig config
   - Lägg till eller uppdatera mcpServers
   - Spara tillbaka

6. **Instruera användaren:**
   - Be dem starta om Claude Desktop
   - Ge test-instruktioner

7. **Rapportera resultat:**
   - Lista vad som installerades
   - Nästa steg för användaren
   - URL till word-cloud (http://localhost:8765/)

---

## 📝 MANUELL KONFIGURATION

Om automatisk installation inte fungerar, följ dessa manuella steg:

1. **Öppna Terminal/PowerShell**

2. **Kör installations-script:**
   - Se "KOMMANDO-SAMMANFATTNING" ovan
   - Kopiera och kör alla kommandon sekventiellt

3. **Redigera Claude Desktop config:**
   - Öppna filen manuellt (sökväg ovan)
   - Kopiera JSON-konfigurationen
   - Spara och stäng

4. **Starta om Claude Desktop**

5. **Testa** enligt "VERIFIERING" ovan

---

## 🆘 SUPPORT

Om problem kvarstår:

1. **Kontrollera Python:**
   ```bash
   which python3  # macOS/Linux
   where python   # Windows
   ```

2. **Kontrollera MCP:**
   ```bash
   pip3 list | grep mcp
   ```

3. **Läs felsökningsguider:**
   - PYTHON_INSTALL.md - Python installation
   - INIT.md - MCP server utveckling
   - README.md - Översikt

4. **Testa manuellt:**
   ```bash
   python3 /Users/spjutbjorn/git/pythonTools/mcp/word-cloud/word_cloud_server.py
   # Ska starta utan fel
   ```

---

## ✨ EFTER INSTALLATION

**Servrarna är nu redo att använda!**

### Large Files Manager
```
Hitta de 20 största filerna i min hemkatalog
Ta bort filen /path/to/large/file.txt
```

### Word Cloud
```
Lägg till ordet "Python" med beskrivning "språk" och storlek 8
Öppna ordmolnet i webbläsaren
```

**Word Cloud URL:** http://localhost:8765/

---

**🎉 Installationen är klar!**

*Nästa steg: Testa servrarna eller skapa din egen MCP-server enligt INIT.md*
