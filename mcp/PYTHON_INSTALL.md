# Python Installation Guide för MCP-servrar

Guide för att installera Python på Mac och Windows, optimerad för att kunna utföras via AI-assistans.

## Innehåll

- [macOS Installation](#macos-installation)
- [Windows Installation](#windows-installation)
- [Verifiering](#verifiering)
- [Virtual Environment Setup](#virtual-environment-setup)
- [Installera MCP Dependencies](#installera-mcp-dependencies)
- [Felsökning](#felsökning)

---

## macOS Installation

### Metod 1: Homebrew (Rekommenderat)

#### Steg 1: Kontrollera om Homebrew är installerat

**Instruktion till AI:**
```
Kör kommandot: which brew
```

Om inget svar kommer, installera Homebrew först (se nedan).

#### Steg 2: Installera Homebrew (om det behövs)

**Instruktion till AI:**
```
Kör kommandot: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Steg 3: Installera Python via Homebrew

**Instruktion till AI:**
```
Kör kommandot: brew install python@3.11
```

eller för senaste versionen:
```
Kör kommandot: brew install python3
```

#### Steg 4: Uppdatera PATH (om nödvändigt)

**Instruktion till AI:**
```
Lägg till följande i min ~/.zshrc eller ~/.bash_profile:
export PATH="/opt/homebrew/bin:$PATH"

Sedan kör: source ~/.zshrc
```

### Metod 2: python.org Installer

1. **Instruktion till AI:**
   ```
   Gå till https://www.python.org/downloads/macos/ och hämta senaste versionen
   ```

2. Ladda ner `.pkg` filen och kör installern
3. Följ installationsguiden
4. Installern lägger till Python automatiskt i PATH

### Metod 3: pyenv (För avancerade användare)

**Instruktion till AI:**
```
Installera pyenv:
brew install pyenv

Lägg till i ~/.zshrc:
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

Installera Python:
pyenv install 3.11.7
pyenv global 3.11.7
```

---

## Windows Installation

### Metod 1: Microsoft Store (Enklast)

**Instruktion till AI:**
```
Jag använder Windows. Hjälp mig öppna Microsoft Store och sök efter "Python 3.11" eller "Python 3.12"
```

1. Öppna Microsoft Store
2. Sök efter "Python 3.11" eller "Python 3.12"
3. Klicka "Get" / "Hämta"
4. Vänta på installation
5. Python läggs automatiskt till i PATH

### Metod 2: python.org Installer

**Instruktion till AI:**
```
Gå till https://www.python.org/downloads/windows/ och hämta senaste Windows installer
```

**VIKTIGT:** När du kör installern:
1. ✅ **Markera "Add Python to PATH"** (längst ner i installern)
2. Välj "Install Now" eller "Customize installation"
3. Om du väljer Customize:
   - ✅ Markera "pip"
   - ✅ Markera "py launcher"
   - ✅ Markera "Add Python to environment variables"

### Metod 3: Chocolatey (För avancerade användare)

**Instruktion till AI:**
```
Jag vill installera Python via Chocolatey. Hjälp mig med:

1. Installera Chocolatey först (kör PowerShell som Admin):
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

2. Installera Python:
choco install python311
```

### Metod 4: winget (Windows Package Manager)

**Instruktion till AI:**
```
Installera Python via winget:
winget install Python.Python.3.11
```

---

## Verifiering

### Kontrollera Python Installation

**Instruktion till AI:**
```
Verifiera att Python är installerat:

macOS/Linux:
python3 --version

Windows:
python --version
eller
py --version
```

Förväntat resultat: `Python 3.11.x` eller `Python 3.12.x`

### Kontrollera pip Installation

**Instruktion till AI:**
```
Verifiera att pip är installerat:

macOS/Linux:
pip3 --version

Windows:
pip --version
eller
py -m pip --version
```

Förväntat resultat: `pip 23.x.x` eller senare

### Kontrollera Python Path

**Instruktion till AI:**
```
Visa var Python är installerat:

macOS/Linux:
which python3
which pip3

Windows (PowerShell):
where.exe python
where.exe pip
```

---

## Virtual Environment Setup

Virtual environments isolerar Python-paket för olika projekt.

### Skapa Virtual Environment

**Instruktion till AI:**
```
Navigera till mitt projekt och skapa en virtual environment:

macOS/Linux:
cd /Users/spjutbjorn/git/pythonTools/mcp
python3 -m venv .venv

Windows:
cd C:\Users\YourName\path\to\mcp
python -m venv .venv
```

### Aktivera Virtual Environment

**Instruktion till AI:**
```
Aktivera virtual environment:

macOS/Linux:
source .venv/bin/activate

Windows (Command Prompt):
.venv\Scripts\activate.bat

Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

**OBS:** Om PowerShell ger felmeddelande om execution policy:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Deaktivera Virtual Environment

**Instruktion till AI:**
```
Deaktivera virtual environment:
deactivate
```

---

## Installera MCP Dependencies

### Installation i Virtual Environment (Rekommenderat)

**Instruktion till AI:**
```
Aktivera virtual environment först, sedan:

cd /Users/spjutbjorn/git/pythonTools/mcp/large-files-manager
pip install -r requirements_large_files.txt

eller installera direkt:
pip install mcp>=1.0.0
```

### Installation Globalt (System-wide)

**Instruktion till AI:**
```
macOS/Linux:
pip3 install mcp>=1.0.0

Windows:
pip install mcp>=1.0.0
```

### Uppgradera pip

Om pip är gammal, uppgradera den:

**Instruktion till AI:**
```
macOS/Linux:
pip3 install --upgrade pip

Windows:
python -m pip install --upgrade pip
```

### Installera alla requirements

**Instruktion till AI:**
```
Installera alla dependencies från requirements-filen:

pip install -r requirements_large_files.txt
```

---

## Felsökning

### Problem: "python not found" eller "command not found"

#### macOS/Linux:

**Instruktion till AI:**
```
Försök:
python3 --version

Om det inte fungerar, hitta Python:
ls /usr/local/bin/python*
ls /opt/homebrew/bin/python*

Lägg till i PATH:
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

#### Windows:

**Instruktion till AI:**
```
1. Försök: py --version
2. Om det inte fungerar, lägg till Python manuellt i PATH:
   - Hitta Python installation (vanligtvis):
     C:\Users\YourName\AppData\Local\Programs\Python\Python311
   - Lägg till i System Environment Variables:
     - Python-mappen
     - Python\Scripts-mappen
```

### Problem: "pip not found"

**Instruktion till AI:**
```
Installera pip manuellt:

macOS/Linux:
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py

Windows:
py get-pip.py
```

### Problem: Permission Denied (macOS/Linux)

**Instruktion till AI:**
```
Använd --user flag:
pip3 install --user mcp

eller använd virtual environment (rekommenderat)
```

### Problem: SSL Certificate Error

**Instruktion till AI:**
```
macOS:
/Applications/Python\ 3.11/Install\ Certificates.command

eller installera certifi:
pip3 install --upgrade certifi
```

### Problem: Multiple Python Versions

**Instruktion till AI:**
```
Lista alla Python-versioner:

macOS:
ls -l /usr/local/bin/python*
ls -l /opt/homebrew/bin/python*

Windows:
py --list

Använd specifik version:
python3.11 --version
py -3.11 --version
```

### Problem: Virtual Environment Activation (PowerShell)

**Instruktion till AI:**
```
Om .venv\Scripts\Activate.ps1 inte fungerar:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Försök igen:
.venv\Scripts\Activate.ps1
```

---

## Snabbkommando-referens

### macOS/Linux

```bash
# Installera Python
brew install python3

# Kontrollera version
python3 --version
pip3 --version

# Skapa virtual environment
python3 -m venv .venv

# Aktivera virtual environment
source .venv/bin/activate

# Installera paket
pip3 install mcp

# Deaktivera virtual environment
deactivate
```

### Windows

```powershell
# Installera Python (Microsoft Store eller winget)
winget install Python.Python.3.11

# Kontrollera version
python --version
pip --version

# Skapa virtual environment
python -m venv .venv

# Aktivera virtual environment
.venv\Scripts\Activate.ps1

# Installera paket
pip install mcp

# Deaktivera virtual environment
deactivate
```

---

## Nästa Steg efter Installation

1. **Verifiera installation:**
   ```
   python3 --version  # macOS/Linux
   python --version   # Windows
   ```

2. **Installera MCP:**
   ```
   pip3 install mcp  # macOS/Linux
   pip install mcp   # Windows
   ```

3. **Testa MCP-server:**
   ```
   python3 /Users/spjutbjorn/git/pythonTools/mcp/word-cloud/word_cloud_server.py
   ```

4. **Konfigurera Claude Desktop:**
   - Se `README.md` eller `INIT.md`

---

## AI-Instruktioner Cheat Sheet

### För Installation

**macOS:**
```
Installera Python på min Mac via Homebrew:
1. Kontrollera om brew finns: which brew
2. Installera Python: brew install python3
3. Verifiera: python3 --version
```

**Windows:**
```
Installera Python på min Windows-dator via Microsoft Store:
1. Öppna Microsoft Store
2. Sök efter "Python 3.11"
3. Installera
4. Verifiera i PowerShell: python --version
```

### För MCP Setup

```
Sätt upp MCP-miljön:
1. Navigera till: /Users/spjutbjorn/git/pythonTools/mcp/large-files-manager
2. Installera requirements: pip3 install -r requirements_large_files.txt
3. Verifiera: python3 -c "import mcp; print('MCP installed')"
```

### För Virtual Environment

```
Skapa och aktivera virtual environment:
1. cd /Users/spjutbjorn/git/pythonTools/mcp
2. python3 -m venv .venv
3. source .venv/bin/activate  (macOS)
   eller
   .venv\Scripts\Activate.ps1  (Windows)
4. pip install mcp
```

---

## Resurser

- [Python Official Downloads](https://www.python.org/downloads/)
- [Homebrew](https://brew.sh/)
- [Python Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html)
- [pip Documentation](https://pip.pypa.io/en/stable/)

---

**Lycka till med installationen! 🐍**

*För hjälp, be din AI-assistent köra kommandona ovan.*
