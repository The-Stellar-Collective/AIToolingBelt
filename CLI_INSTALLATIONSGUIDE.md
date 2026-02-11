# Installation av AI-verktyg (CLI & Desktop Apps)

Denna guide beskriver hur man installerar och använder Claude CLI, ChatGPT CLI, Google Gemini CLI, samt Desktop Apps för Claude och ChatGPT (Codex) på Mac, Windows och Linux.

---

## Innehållsförteckning

### Desktop Apps
1. [Claude Desktop App](#claude-desktop-app)
2. [ChatGPT Desktop App (Codex)](#chatgpt-desktop-app-codex)

### CLI-verktyg
3. [Claude CLI](#claude-cli)
4. [ChatGPT CLI](#chatgpt-cli)
5. [Google Gemini CLI](#google-gemini-cli)

### Övriga
6. [Grundkrav per plattform](#grundkrav-per-plattform)
7. [Snabstart](#snabstart)

---

## Claude Desktop App

Claude Desktop App är Anthropic's officiella desktop-applikation för att använda Claude direkt på din dator med ett modernt gränssnitt.

### Grundkrav
- macOS 11+ eller Windows 10+
- Claude-konto (gratis eller betald)
- Internet-anslutning
- Minst 512 MB ledigt RAM

### Installation på Mac

```bash
# Via Homebrew
brew install claude

# Eller ladda ned från
# https://claude.ai/download

# Starta appen
open /Applications/Claude.app
```

**Eller manuell download:**
1. Gå till https://claude.ai/download
2. Ladda ned Claude.dmg
3. Dra Claude till Applications-mappen
4. Dubbelklicka på Claude för att starta

### Installation på Windows (PC)

1. Gå till https://claude.ai/download
2. Ladda ned Claude-Installer.exe
3. Kör installationsfilen
4. Följ installationsguiden
5. Starta Claude från Start-menyn

**Via Chocolatey:**
```powershell
choco install claude
```

### Installation på Linux

Claude Desktop App är främst tillgänglig för Mac och Windows. För Linux kan du använda:
- **Web-versionen**: https://claude.ai (i webbläsaren)
- **Claude CLI**: `npm install -g @anthropic-ai/claude-code`

### Använd Claude Desktop App

```
1. Starta appen
2. Logga in med ditt Claude-konto
3. Börja chatta direkt
4. Ladda upp filer för analys
5. Använd menyerna för att anpassa inställningar
```

---

## ChatGPT Desktop App (Codex)

ChatGPT Desktop App är OpenAI's officiella app för att använda ChatGPT och Codex direkt på din dator.

### Grundkrav
- macOS 11+ eller Windows 10+
- OpenAI-konto (gratis eller betald)
- Internet-anslutning
- Minst 512 MB ledigt RAM

### Installation på Mac

```bash
# Via Homebrew
brew install chatgpt

# Eller ladda ned från
# https://openai.com/chatgpt/download

# Starta appen
open /Applications/ChatGPT.app
```

**Eller manuell download:**
1. Gå till https://openai.com/chatgpt/download
2. Ladda ned ChatGPT.dmg
3. Dra ChatGPT till Applications-mappen
4. Dubbelklicka på ChatGPT för att starta

### Installation på Windows (PC)

1. Gå till https://openai.com/chatgpt/download
2. Ladda ned ChatGPT-Installer.exe
3. Kör installationsfilen
4. Följ installationsguiden
5. Starta ChatGPT från Start-menyn

**Via Chocolatey:**
```powershell
choco install chatgpt
```

### Installation på Linux

ChatGPT Desktop App är främst tillgänglig för Mac och Windows. För Linux kan du använda:
- **Web-versionen**: https://chatgpt.com (i webbläsaren)
- **ChatGPT CLI**: `npm install -g chatgpt`

### Använd ChatGPT Desktop App

```
1. Starta appen
2. Logga in med ditt OpenAI-konto
3. Börja chatta direkt
4. Använd Codex för kodgenering
5. Ladda upp filer för analys
6. Aktivera voice mode för tal-input/output
```

---

## Claude CLI

Claude CLI är Anthropic's officiella kommandoradsverktyg för att interagera med Claude AI-modellen direkt från terminalen.

### Grundkrav
- Node.js 18+ eller Homebrew (Mac)
- Internet-anslutning
- Claude-konto (gratis eller betald)

### Installation på Mac

```bash
# Via Homebrew (snabbaste)
brew install claude-code

# Eller via npm
npm install -g @anthropic-ai/claude-code

# Verifiera installation
claude --version
```

### Installation på Windows (PC)

```powershell
# Via npm (kräver Node.js)
npm install -g @anthropic-ai/claude-code

# Verifiera installation
claude --version
```

**Eller ladda ned installationsfil från:** https://github.com/anthropics/claude-code

### Installation på Linux

```bash
# Via npm
npm install -g @anthropic-ai/claude-code

# Eller från källan
git clone https://github.com/anthropics/claude-code.git
cd claude-code
npm install -g .

# Verifiera installation
claude --version
```

### Starta Claude CLI

```bash
# Öppna interaktiv session
claude

# Eller arbeta med en fil
claude script.py

# Visa hjälp
claude --help

# Visa version
claude --version
```

**Primera gång du startar:** Claude autentiserar dig genom att öppna webbläsaren automatiskt.

---

## ChatGPT CLI

ChatGPT CLI är ett officiellt kommandoradsverktyg för att interagera med ChatGPT och GPT-modeller från terminalen.

### Grundkrav
- Node.js 18+ eller Python 3.8+
- npm eller pip pakethanterare
- OpenAI-konto (gratis eller betald)
- Internet-anslutning

### Installation på Mac

```bash
# Via npm (rekommenderat)
npm install -g chatgpt

# Eller via Homebrew
brew install chatgpt-cli

# Verifiera installation
chatgpt --version
```

### Installation på Windows (PC)

```powershell
# Via npm (kräver Node.js)
npm install -g chatgpt

# Verifiera installation
chatgpt --version
```

**Eller ladda ned från:** https://github.com/transitive-bullshit/chatgpt-cli

### Installation på Linux

```bash
# Via npm
npm install -g chatgpt

# Eller från källan
git clone https://github.com/transitive-bullshit/chatgpt-cli.git
cd chatgpt-cli
npm install -g .

# Verifiera installation
chatgpt --version
```

### Starta ChatGPT CLI

```bash
# Öppna interaktiv session
chatgpt

# Eller ställ en direkt fråga
chatgpt "Vad är artificiell intelligens?"

# Skicka meddelande från fil
chatgpt < prompt.txt

# Visa hjälp
chatgpt --help

# Visa version
chatgpt --version
```

**Primera gången du startar:** ChatGPT autentiserar dig genom att öppna webbläsaren automatiskt.

---

## Google Gemini CLI

Google Gemini CLI är ett officiellt kommandoradsverktyg för att interagera med Google's Gemini AI-modeller.

### Grundkrav
- Python 3.8+
- pip pakethanterare
- Google-konto (gratis eller betald)
- Internet-anslutning

### Installation på Mac

```bash
# Via pip
pip install google-generativeai-cli

# Eller från GitHub
pip install git+https://github.com/google/generative-ai-python.git

# Verifiera installation
gemini --version
```

### Installation på Windows (PC)

```powershell
# Via pip
pip install google-generativeai-cli

# Verifiera installation
gemini --version
```

### Installation på Linux

```bash
# Via pip
pip install google-generativeai-cli

# Verifiera installation
gemini --version
```

### Starta Gemini CLI

```bash
# Öppna interaktiv session
gemini

# Eller kör med prompt
gemini "Din fråga här"

# Visa hjälp
gemini --help

# Visa version
gemini --version
```

**Primera gången:** Gemini öppnar webbläsaren för autentisering med ditt Google-konto.

---

## Grundkrav per plattform

### Mac (macOS)

**Minimalt:**
- macOS 10.13 eller senare
- Terminal eller valfri terminal-emulator

**För Claude CLI:**
```bash
brew install claude-code
```

**För ChatGPT CLI:**
```bash
npm install -g chatgpt
```

**För Gemini CLI:**
```bash
pip install google-generativeai-cli
```

**För Claude Desktop App:**
```bash
brew install claude
```

**För ChatGPT Desktop App:**
```bash
brew install chatgpt
```

**Pakethanterare:**
```bash
# Homebrew (om inte redan installerad)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Windows (PC)

**Minimalt:**
- Windows 10 eller senare
- PowerShell eller Command Prompt

**För Claude CLI:**
```powershell
npm install -g @anthropic-ai/claude-code
```

**För ChatGPT CLI:**
```powershell
npm install -g chatgpt
```

**För Gemini CLI:**
```powershell
pip install google-generativeai-cli
```

**För Claude Desktop App:**
```powershell
choco install claude
```

**För ChatGPT Desktop App:**
```powershell
choco install chatgpt
```

**Pakethanterare:**
- **Node.js + npm:** https://nodejs.org/
- **Python + pip:** https://www.python.org/ (markera "Add to PATH")
- **Chocolatey:** https://chocolatey.org/install

### Linux

**Minimalt:**
- Linux-distribution (Ubuntu, Debian, Fedora, etc.)
- bash eller zsh
- sudo-åtkomst (för paketinstallation)

**För Claude CLI:**
```bash
npm install -g @anthropic-ai/claude-code
```

**För ChatGPT CLI:**
```bash
npm install -g chatgpt
```

**För Gemini CLI:**
```bash
pip install google-generativeai-cli
```

**För Claude Desktop App & ChatGPT Desktop App:**
Desktop Apps är inte tillgängliga för Linux. Använd CLI-verktygen eller web-versionerna istället.

**Pakethanterare - Installation:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install nodejs npm python3-pip curl git

# Fedora/RHEL
sudo dnf install nodejs npm python3-pip curl git

# Arch
sudo pacman -S nodejs npm python pip curl git
```

---

## Snabstart

### Claude CLI - 2 steg

```bash
1. brew install claude-code        # Mac
   npm install -g @anthropic-ai/claude-code  # Windows/Linux

2. claude                           # Starta interaktiv session
```

### ChatGPT CLI - 2 steg

```bash
1. npm install -g chatgpt

2. chatgpt                          # Starta interaktiv session
```

### Gemini CLI - 2 steg

```bash
1. pip install google-generativeai-cli

2. gemini                           # Starta interaktiv session
```

### Claude Desktop App - 1 steg

```bash
1. brew install claude              # Mac
   # eller ladda ned från https://claude.ai/download
```

### ChatGPT Desktop App (Codex) - 1 steg

```bash
1. brew install chatgpt             # Mac
   # eller ladda ned från https://openai.com/chatgpt/download
```

---

## Snabbkommandon

### Claude
```bash
claude                    # Interaktiv session
claude code.py           # Analysera fil
claude --help            # Hjälp
```

### ChatGPT
```bash
chatgpt                           # Interaktiv session
chatgpt "Vad är 2+2?"            # Direkt fråga
chatgpt < prompt.txt             # Läs från fil
chatgpt --help                   # Hjälp
```

### Gemini
```bash
gemini                   # Interaktiv session
gemini "Vad är 2+2?"    # Direkt fråga
gemini --help           # Hjälp
```

### Claude Desktop App
```
Starta appen och börja chatta direkt
Logga in vid första användning
Ladda upp filer via chat-gränssnittet
```

### ChatGPT Desktop App (Codex)
```
Starta appen och börja chatta direkt
Logga in vid första användning
Använd Codex för kodgenering
Aktivera voice mode för tal-input/output
```

---

## Autentisering

Alla verktyg använder säker webbaserad autentisering:

**CLI-verktyg:**
1. Primera gång du startar: Det öppnas automatiskt en webbläsare
2. Du loggar in med ditt konto (Claude, ChatGPT eller Google)
3. Sessionen sparas lokalt - ingen manuell nyckelhantering behövs
4. Du kan börja använda direkt

**Desktop Apps:**
1. Starta appen
2. Du dirigeras till webbläsare för inloggning
3. Tillåt att appen öppnas efter inloggning
4. Appen är nu autentiserad och redo att använda

---

## Felsökning

### "Command not found"
```bash
# Kontrollera installation
which claude          # Mac/Linux
where claude          # Windows

# Installera om
npm install -g @anthropic-ai/claude-code
```

### Autentiseringsfel
```bash
# Logga ut och in igen
claude logout
claude login

# Eller för Codex
gh auth logout
gh auth login
```

### Port redan i användning
```bash
# Ange annan port (om möjligt)
claude --port 3001
```

### Internet-problem
```bash
# Kontrollera anslutning
ping google.com

# Testa firewall-inställningar
```

---

## Uppdatera installationerna

```bash
# Claude
npm update -g @anthropic-ai/claude-code

# Gemini
pip install --upgrade google-generativeai-cli

# Codex
gh extension upgrade gh-copilot
```

---

## Officiella webbplatser

- **Claude:** https://claude.ai | Download: https://claude.ai/download
- **ChatGPT/Codex:** https://chatgpt.com | Download: https://openai.com/chatgpt/download
- **Gemini:** https://gemini.google.com

---

*Uppdaterad: 2026-02-11*
