# BetterCMD

**BetterCMD** is an enhanced alternative to the default Windows Command Prompt, developed by **Delta Studios**. It adds useful features, a friendlier interface, and even an integrated AI assistant to your command line experience.

## 🚀 Features

- **AXIOM AI Assistant**  
  Built-in smart assistant powered by Google Gemini (via API). Ask questions directly from your terminal.

- **NaVi Editor**  
  A Textual-based GUI code editor inspired by Vim. Supports:
  - Undo/redo
  - Auto-close brackets
  - Line numbering
  - Cursor control with arrow keys
  - File saving and editing

- **Custom Functions System**  
  Define your own custom Python or Batch functions in a JSON file and run them directly via CLI.

- **ZIP / UNZIP Tools**  
  Compress or extract files quickly with custom CLI commands. Optional flag to delete originals.

- **Image to ASCII Converter**  
  Converts grayscale images to ASCII art for fun or creative terminal visuals.

- **Base Encoder/Decoder**  
  Supports Base16, Base32, Base64, and Base85 encoding/decoding for any string.

- **Beep Music**  
  Generate tones using note names (like C4, A5) with customizable duration and volume.

- **IP Info Lookup**  
  Get detailed information about your own or other public IP addresses.

- **Command Auto-Completion**  
  Press `Tab` to autocomplete built-in BetterCMD commands.

## 📁 File Structure (Generated on First Launch)
```
userfiles/
├── .startup # Runs commands on startup
├── axiom.txt # Stores the Google Gemini API key
├── cfunc.json # Custom functions storage (Python/Batch)
├── history.log # Logs all commands
└── user.json # Stores encoded username, password, and creation date
```


## 🛠 Installation & Setup

1. Run `bettercmd.py` using Python 3.10+.
2. On first run, it will prompt you to create a username and password.
3. (Optional) Enter your Google Gemini API key in `userfiles/axiom.txt` to use AXIOM AI.

## 💡 Tip

Run BetterCMD in **Maximized or Fullscreen mode** for the best visual experience.

## 📃 License & More Info

- License: See `LICENSE`
- Docs: See `README` or visit the GitHub repository  
- GitHub: https://github.com/DeltaStudios01/BetterCMD
