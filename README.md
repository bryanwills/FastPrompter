<div align="center">
  <img src="https://raw.githubusercontent.com/vacterro/FastPrompter/main/_res/fastprompter_logo1.png" alt="FastPrompter Logo" width="128" height="128"/>
  <h1 align="center">FastPrompter</h1>
  <p align="center">
    <strong>Blazing-fast portable snippet manager & scratchpad for Windows</strong>
  </p>
  <p align="center">
    One hotkey. Instant window. Your prompts, snippets, and drafts — always one keystroke away.
  </p>
  <p align="center">
    <a href="https://github.com/vacterro/FastPrompter/releases">
      <img src="https://img.shields.io/github/v/release/vacterro/FastPrompter?style=for-the-badge&label=Download&color=brightgreen" alt="Download"/>
    </a>
    <a href="LICENSE">
      <img src="https://img.shields.io/github/license/vacterro/FastPrompter?style=for-the-badge&color=blue" alt="MIT License"/>
    </a>
    <a href="https://www.python.org/downloads/">
      <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11+"/>
    </a>
    <img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logoColor=white" alt="Windows"/>
    <img src="https://img.shields.io/badge/100%25-Portable-important?style=for-the-badge" alt="Portable"/>
  </p>
  <br>
  <img width="960" height="540" alt="FastPrompter main window" src="https://github.com/user-attachments/assets/7839fd84-3e3b-4062-bfb4-21729bfc514b" />
</div>

---

## ✨ Features

### ⚡ Core

| | Feature | Details |
|---|---------|---------|
| ⚡ | **Instant Access** | Global hotkey (`Alt+X`, alt bind `F15`) — window appears at your cursor |
| 🗄️ | **Silo System** | Up to 100 persistent scratch slots per project — your always-saved drafts |
| 📋 | **Snippet Engine** | Named snippets per project tab, `F1`–`F10` instant paste |
| 🗂️ | **Projects** | Up to 5 project tabs, each with its own snippets, silos, and archive |
| 📦 | **Archive** | One button archives the current silo *or* snippet — never lose a draft |
| 💾 | **Auto-Save** | Real-time SQLite persistence — close it, kill it, your text survives |

### 🖱️ Interaction

| | Feature | Details |
|---|---------|---------|
| 🖱️ | **Wheel Everything** | Mouse wheel pages silos, snippets, archive; switches tabs; `Ctrl+wheel` zooms |
| 📌 | **Pin & Archive on Hover** | Hover a silo → 📌 pin-to-top and 📥 archive buttons appear |
| 🎨 | **Last-Edited Colors** | Silos tint by recency — spot your freshest draft at a glance |
| 🔢 | **Line Counters** | Per-silo line count at the sidebar edge + live counter in the header |
| 🤏 | **Smart Drag & Drop** | Drop a silo *between* others to reorder, *onto* one to swap |
| 📄 | **Drop Any File** | Drag ~50 text-based file types into the editor — loads as pasted text |
| ⌨️ | **Keyboard Silo Nav** | `Alt+Up` / `Alt+Down` walks the sidebar without touching the mouse |
| 🔗 | **Clickable Links** | URLs in your text open in the browser |

### ✍️ Editor

| | Feature | Details |
|---|---------|---------|
| 🔤 | **Markdown Toolbar** | Bold / Italic / Underline / Strike, header + timestamp (`Ctrl+E`) |
| ➖ | **Smart Dividers** | `Ctrl+W` inserts a spaced `---` rule, rendered as a real line |
| • | **Auto-Bullet** | `-` + space becomes `•`, Enter continues the list, Enter again ends it |
| ☑️ | **Checkboxes** | `[ ]` renders as a real clickable checkbox, `Ctrl+Return` toggles |
| 🦓 | **Zebra Stripes** | Subtle alternating line contrast — toggleable, color & opacity configurable |
| 📏 | **Line Numbers** | Toggleable gutter with clickable margin marks (🔴 → 🟦 → 🔺 → off) |
| 🔍 | **Find & Replace** | `Ctrl+F` / `Ctrl+H`, Esc closes search first, hides window second |
| 👁️ | **Preview Modes** | Source, live markdown highlighting, or rendered reading view |

### 🎛️ Window & Polish

| | Feature | Details |
|---|---------|---------|
| 🎨 | **Themes** | 6 vintage-inspired themes + full custom color editor |
| 🎵 | **Sound FX** | Configurable UI sounds + optional typewriter effect while typing |
| 🌙 | **Focus Mode** | `Ctrl+D` — minimal zen interface |
| 🔐 | **Lock Mode** | Lock window position/size; lock-to-cursor summoning |
| 🎯 | **Snap Corners** | `Ctrl+Q` cycles the window through screen corners |
| 🪟 | **Edge Resize** | Frameless window, drag any edge or corner |
| ⌨️ | **Dual Hotkeys** | Every global bind has a primary *and* an alternative slot |

## 🚀 Quick Start

### Option 1: Portable EXE (Recommended)

1. Grab the latest from **[Releases →](https://github.com/vacterro/FastPrompter/releases)**
2. Run it — **no installation, no Python, no admin rights**
3. Press **`Alt+X`**

> 💡 **100% portable:** the database lives in a `data/` folder next to the EXE. Run it from a USB stick, a network share, anywhere — your data travels with the app.

### Option 2: Run from Source

```powershell
git clone https://github.com/vacterro/FastPrompter.git
cd FastPrompter

# with uv (recommended)
uv sync
uv run python FastPrompter.pyw

# or with pip
pip install -r requirements.txt
python FastPrompter.pyw
```

### Build Your Own EXE

```powershell
pip install -e .[build]     # installs Nuitka
python tools/build.py       # → build/FastPrompter.exe
```

The build prunes unused Qt plugins and skips QtMultimedia's ~100 MB FFmpeg payload entirely — sounds play through a lightweight native fallback. Install [UPX](https://upx.github.io/) for further compression.

## ⌨️ Key Bindings

### Global Hotkeys (rebindable, two slots each)

| Key | Action |
|-----|--------|
| `Alt+X` / `F15` | Toggle window |
| `Shift+Alt+X` | Quick List (pie menu) |
| `Alt+D` | Toggle sidebar |
| `Ctrl+Shift+L` | Lock / unlock window |
| `Ctrl+Shift+E` | Always on top |

### In-App

| Key | Action |
|-----|--------|
| `Ctrl+N` | New empty silo (capped at 5 blanks — no spam) |
| `Alt+Up` / `Alt+Down` | Previous / next silo |
| `Ctrl+1`–`Ctrl+0` | Jump to silo 1–10 |
| `F1`–`F10` | Paste snippet 1–10 |
| `Ctrl+S` | Save / update snippet |
| `Ctrl+W` | Insert divider line |
| `Ctrl+E` | Header + timestamp on current line |
| `Ctrl+Return` | Toggle checkboxes |
| `Ctrl+B` / `I` / `U` | Bold / Italic / Underline |
| `Ctrl+F` / `Ctrl+H` | Find / Replace |
| `Ctrl+Z` / `Ctrl+Shift+Z` | Undo / Redo |
| `Ctrl+Q` | Cycle snap corners |
| `Ctrl+D` | Focus mode |
| `Ctrl+Shift+S` | Export silo to file |
| `Esc` | Close search → hide & save |
| `Ctrl+Alt+Shift+Q` | Quit completely |

### Mouse

| Gesture | Action |
|---------|--------|
| Wheel over silos / snippets / archive | Flip pages |
| Wheel over tab bar | Switch project |
| `Ctrl` + wheel in editor | Zoom font |
| Middle-click a silo | Clear it (empty silo → delete the slot) |
| Hover a silo | Reveal 📌 pin / 📥 archive buttons |
| Right-click a silo | Full menu: transfer to project, replace from, move to bottom… |
| Left / right half-click a snippet | Open with cursor at start / end |

## 📸 Screenshots

<div align="center">
  <img width="960" height="540" alt="Editor with sidebar" src="https://github.com/user-attachments/assets/5f964283-8cba-4d68-80a7-9e0658e66f43" />
  <img width="960" height="540" alt="Snippet management" src="https://github.com/user-attachments/assets/d7c5e7d1-72fa-4fd4-a5f4-cd7aa71bc540" />
  <img width="960" height="540" alt="Theme gallery" src="https://github.com/user-attachments/assets/1e06c770-9fd9-4f8a-8358-068fab4aca29" />
  <img width="960" height="540" alt="Settings" src="https://github.com/user-attachments/assets/a10668b7-0c17-4b01-97ed-81276b311c2a" />
  <img width="960" height="539" alt="Quick list" src="https://github.com/user-attachments/assets/d4d9e0ec-0c84-4a23-8a2d-635ce1079193" />
  <img width="960" height="540" alt="Focus mode" src="https://github.com/user-attachments/assets/28375f37-f80c-4817-9bea-03f9901e9ee2" />
</div>

## 🎨 Themes

| Theme | Style |
|-------|-------|
| **Default** | Dark vintage — warm amber on black |
| **Golden Vintage** | Rich gold & brown — classic terminal vibes |
| **Golden Default** | Warm gold tones, balanced contrast |
| **Vintage Dark** | Deep charcoal with muted accents |
| **Vintage Classic** | Windows 95 retro — raised 3D bevels |
| **Dark 2 (OLED)** | Pure black, maximum contrast |
| **Custom** | Full color picker, including last-edited overlay colors |

## 📁 Data & Portability

FastPrompter stores everything locally — **no cloud, no telemetry, no accounts**.

| Item | Location |
|------|----------|
| **Database** | `data/local_data_v15.db` — next to the EXE, fully portable |
| **Markdown Backups** | `Documents\.fastprompter\YYYY-MM-DD\` — silos, archive & snippets as structured `.md` files, 7-day rotation (on by default, toggleable) |
| **Crash Log** | `crash.log` next to the EXE — crashes are loud, never silent |

The backup mirror means your content is always readable as plain Markdown files, even without FastPrompter installed.

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.11+ |
| GUI | PyQt6 6.8+ — frameless, custom-drawn |
| Storage | SQLite via stdlib `sqlite3`, transactional diff-based saves |
| Global Hotkeys | Win32 `RegisterHotKey` |
| Sound | `QSoundEffect` with stdlib `winsound` fallback (keeps builds ~100 MB lighter) |
| Markdown | Custom `QSyntaxHighlighter` |
| Packaging | Nuitka single-file EXE, Qt-plugin pruning + optional UPX |

## 🧪 Tests

```powershell
uv run pytest tests/        # 461 unit tests (mocked Qt)
uv run pytest tests_smoke/  # 20 integration tests — boots the real app offscreen
uv run ruff check src/ tests/ tests_smoke/
```

The smoke suite constructs the actual `FastPrompter` window against a temp database and drives silo switching, pinning, drag-reorder remapping, auto-bullet, wheel paging, sounds, zebra/line-number painting, and more. Both suites run in CI on every push.

## 📐 Architecture

```
FastPrompter/
├── FastPrompter.pyw            # Entry point + Nuitka build directives
├── src/fastprompter/
│   ├── main.py                 # FastPrompter window — composition root
│   ├── core/                   # Headless logic
│   │   ├── state.py            #   SQLite persistence (diff-based writes)
│   │   ├── sound_manager.py    #   Sound FX with graceful fallback
│   │   ├── hotkeys.py          #   Win32 hotkey parsing
│   │   ├── hotkey_filter.py    #   Native event filter (WM_HOTKEY)
│   │   └── ipc_server.py       #   Single-instance IPC
│   ├── ui/                     # Widgets + behavior mixins
│   │   ├── editor.py           #   VaultTextEdit — zebra, checkboxes, gutter
│   │   ├── snippet_panel.py    #   Silo/snippet buttons, drag & drop, WheelPager
│   │   ├── *_mixin.py          #   Formatting, theming, scaling, search, tray…
│   │   └── settings.py         #   Color & hotkey dialogs
│   ├── theme/                  # Theme definitions + custom theme generator
│   ├── utils/                  # Portable path resolution, markdown backup
│   └── sound/                  # WAV sound effects
├── _res/                       # Icons & branding
├── tests/                      # Unit suite
├── tests_smoke/                # Real-PyQt6 integration suite
└── tools/build.py              # Nuitka build script
```

## 📜 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE).

---

<div align="center">
  <sub>Built with Python, PyQt6, and ❤️ — by <a href="https://github.com/vacterro">vacterro</a></sub>
</div>
