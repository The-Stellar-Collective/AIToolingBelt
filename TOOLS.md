# Installation och Setup av Utvecklarverktyg

Denna guide visar hur man installerar och konfigurerar essentiella utvecklarverktyg på Mac, Windows och Linux.

---

## Innehållsförteckning
1. [VS Code Installation](#vs-code-installation)
2. [Markdown Extensions](#markdown-extensions)
3. [Rekommenderade Inställningar](#rekommenderade-inställningar)

---

## VS Code Installation

### Mac (macOS)

#### Metod 1: Via Homebrew (Rekommenderat)

```bash
# Installera VS Code
brew install --cask visual-studio-code

# Verifiera installation
code --version
```

#### Metod 2: Manuell Download

1. Gå till https://code.visualstudio.com/
2. Klicka på "Download for Mac"
3. Välj rätt arkitektur:
   - **Apple Silicon (M1/M2/M3):** Download ARM64
   - **Intel:** Download x64
4. Öppna DMG-filen och dra VS Code till Applications-mappen
5. Dubbelklicka på VS Code för att starta

#### Verifiera Installation

```bash
# Starta VS Code från terminal
code

# Eller öppna en mapp
code /path/to/folder
```

---

### Windows (PC)

#### Metod 1: Via Chocolatey (Rekommenderat)

```powershell
# Installera VS Code
choco install vscode

# Verifiera installation
code --version
```

#### Metod 2: Direktuppladdning från Microsoft

1. Gå till https://code.visualstudio.com/
2. Klicka på "Download for Windows"
3. Kör installationsfilen (VSCodeSetup.exe)
4. Följ installationsguiden
5. **Viktigt:** Markera dessa alternativ:
   - ☑ "Add to PATH" (viktigt för terminal-åtkomst)
   - ☑ "Create desktop icon" (valfritt)
   - ☑ "Add 'Open with Code' action to Windows Explorer file context menu"
   - ☑ "Add 'Open with Code' action to Windows Explorer folder context menu"

#### Verifiera Installation

```powershell
# Öppna VS Code från PowerShell
code

# Eller öppna en mapp
code C:\path\to\folder
```

---

### Linux

#### Ubuntu/Debian

```bash
# Uppdatera paketlistor
sudo apt-get update

# Installera VS Code
sudo apt-get install code

# Verifiera installation
code --version
```

**Via Microsoft Repository (Alternativ):**

```bash
# Lägg till Microsoft-nyckeln
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg

# Lägg till Microsoft-repository
sudo sh -c 'echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'

# Uppdatera och installera
sudo apt-get update
sudo apt-get install code
```

#### Fedora/RHEL

```bash
# Lägg till VS Code-repository
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
sudo sh -c 'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'

# Uppdatera och installera
sudo dnf update
sudo dnf install code
```

#### Arch Linux

```bash
# Installera från AUR
yay -S visual-studio-code-bin

# Eller från community-repo
sudo pacman -S code
```

#### Verifiera Installation

```bash
# Öppna VS Code från terminal
code

# Eller öppna en mapp
code /path/to/folder
```

---

## Markdown Extensions

### Rekommenderade Markdown Extensions

#### 1. **Markdown All in One** (Rekommenderat)

En komplett Markdown-lösning med support för tabeller, listöversikter och mer.

**Installation via GUI:**
1. Öppna VS Code
2. Klicka på **Extensions** icon (eller tryck `Ctrl+Shift+X` / `Cmd+Shift+X`)
3. Sök efter **"Markdown All in One"**
4. Klicka på extension från Yu Zhang
5. Klicka **Install**

**Installation via Terminal:**

```bash
code --install-extension yzhang.markdown-all-in-one
```

**Funktioner:**
- Markdown preview
- Tabell-formatering
- Listöversikt
- Auto-fyll av listor
- Tangentbordsgenvägar
- Math-stöd

---

#### 2. **Markdown Preview Enhanced**

Avancerad preview med Theme-stöd och LaTeX-rendering.

**Installation:**

```bash
code --install-extension shd101wyy.markdown-preview-enhanced
```

**Funktioner:**
- Enhanced preview
- Tema-stöd
- Grafer och diagram (Mermaid, PlantUML)
- LaTeX-matematik
- Export till PDF/HTML/PNG

---

#### 3. **Markdownlint**

Verktyg för att kontrollera Markdown-formatering och stil.

**Installation:**

```bash
code --install-extension davidanson.vscode-markdownlint
```

**Funktioner:**
- Automatisk stil-kontroll
- Regelkonfiguration
- Lint-felmeddelanden
- Snabb-åtgärder

---

#### 4. **Better Markdown**

Förbättrad syntax-highlighting för Markdown.

**Installation:**

```bash
code --install-extension Gitzilla.better-markdown
```

**Funktioner:**
- Bättre färg-highlighting
- Stöd för fler Markdown-dialekter
- Tema-kompatibilitet

---

### Installation av Multiple Extensions

**Installera alla rekommenderade extensions på en gång:**

```bash
code --install-extension yzhang.markdown-all-in-one \
     --install-extension shd101wyy.markdown-preview-enhanced \
     --install-extension davidanson.vscode-markdownlint \
     --install-extension Gitzilla.better-markdown
```

---

## Rekommenderade Inställningar

### Markdown-Specifika Inställningar

Öppna Settings (`Cmd+,` / `Ctrl+,`) och lägg till:

```json
"[markdown]": {
  "editor.defaultFormatter": "yzhang.markdown-all-in-one",
  "editor.formatOnSave": true,
  "editor.wordWrap": "on",
  "editor.lineNumbers": "on",
  "editor.fontSize": 14
},
"markdown.extension.tableFormatter.enable": true,
"markdown.extension.completion.respectMarkdownFileFrontMatter": true,
"markdown.preview.fontSize": 14
```

### Generella VS Code-Inställningar för Utveckling

```json
{
  "editor.formatOnSave": true,
  "editor.wordWrap": "on",
  "editor.tabSize": 2,
  "editor.insertSpaces": true,
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000,
  "editor.minimap.enabled": false,
  "editor.bracketPairColorization.enabled": true,
  "editor.guides.bracketPairs": true,
  "explorer.openEditors.visible": 0
}
```

---

## Användbara Tangentbordsgenvägar för Markdown

### Mac

| Genväg | Åtgärd |
|--------|--------|
| `Cmd+B` | Gör text **bold** |
| `Cmd+I` | Gör text *italic* |
| `Cmd+Shift+V` | Preview Markdown |
| `Cmd+K V` | Preview på sidan (split-view) |
| `Cmd+K Cmd+0` | Fäll ihop alla avsnitt |
| `Cmd+K Cmd+J` | Expandera alla avsnitt |

### Windows/Linux

| Genväg | Åtgärd |
|--------|--------|
| `Ctrl+B` | Gör text **bold** |
| `Ctrl+I` | Gör text *italic* |
| `Ctrl+Shift+V` | Preview Markdown |
| `Ctrl+K V` | Preview på sidan (split-view) |
| `Ctrl+K Ctrl+0` | Fäll ihop alla avsnitt |
| `Ctrl+K Ctrl+J` | Expandera alla avsnitt |

---

## Arbetens Workflow för Markdown-filer

### Snabbt Arbetsflöde

1. **Öppna eller skapa en `.md`-fil:**
   ```bash
   code my-document.md
   ```

2. **Aktivera Preview på sidan:**
   - Mac: `Cmd+K V`
   - Windows/Linux: `Ctrl+K V`

3. **Skriv din Markdown** med auto-completion från Markdown All in One

4. **Kontrollera formatering** med Markdownlint-varningar

5. **Spara automatiskt** (om formatOnSave är aktiverat)

### Användbara Commands

Öppna Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`):

```
> Markdown: Create Table         - Skapa en tabell
> Markdown: Toggle bold          - Gör text bold
> Markdown: Toggle italic        - Gör text italic
> Markdown: Toggle code block    - Skapa kodblock
> Markdown: Create list          - Skapa lista
> Markdown Preview Enhanced: Export... - Exportera till PDF/HTML
```

---

## Felsökning

### VS Code startar inte från terminal

**Mac/Linux:**
```bash
# Lägg till VS Code till PATH
cat >> ~/.zshrc << 'EOF'
export PATH="$PATH:/usr/local/bin"
EOF
source ~/.zshrc
```

**Windows:**
- Kör installationen igen
- Markera "Add to PATH"
- Starta om PowerShell/Command Prompt

### Extensions installeras inte

```bash
# Uppdatera VS Code
code --update

# Installera extension igen
code --install-extension yzhang.markdown-all-in-one
```

### Preview fungerar inte

1. Kontrollera att extension är installerat
2. Öppna Command Palette: `Cmd+Shift+P` / `Ctrl+Shift+P`
3. Sök: `Markdown: Open Preview to the Side`
4. Kör kommandot

### Låg prestanda med stor fil

- Öppna Settings
- Sök: `markdown.preview.breaks`
- Sätt till `false`

---

## Alternativa Editors

Medan VS Code är rekommenderat, kan du också använda:

- **Sublime Text** - Snabb och lätt
- **Atom** - GitHub's editor (begränsad support)
- **Vim/Neovim** - Terminal-baserad
- **Obsidian** - Fokuserad på Markdown-anteckningar
- **Typora** - Minimalistisk Markdown-editor

---

## Resurser

- **VS Code Dokumentation:** https://code.visualstudio.com/docs
- **Markdown Guide:** https://www.markdownguide.org/
- **Markdown All in One:** https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one
- **Markdownlint Rules:** https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md

---

*Sista uppdatering: 2026-02-11*
