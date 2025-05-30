# ./src/bettercmd.py

# importing some modules
import os, platform, sys, json, base64
from datetime import datetime
import time; delay = time.sleep
from rich.panel import Panel ; from rich.align import Align ; from rich.console import Console as _Console ; console = _Console() ; from rich.markdown import Markdown
import numpy as np ; import pyaudio
import subprocess
import readline, logging; from typing import Literal
import google.generativeai as ai
from textual.app import App, ComposeResult
from textual.widgets import Static, Footer, Header
from textual.containers import Vertical
from textual.events import Key
from rich.text import Text
from tkinter import messagebox as msgbox
import win32gui
import win32con
import win32api
from PIL import Image
import requests
import zipfile

# creating 'usefiles' folder
if not os.path.exists("userfiles"):
    os.makedirs("userfiles")

# --- axiom file creating ---
AXIOM_FILE = "userfiles\\axiom.txt"
if not os.path.exists(AXIOM_FILE): 
    with open(AXIOM_FILE, "w") as f:
        f.write("// This is axiom.txt you can put Google Gemini's API here.\n")
        f.write("// Get the API here: https://aistudio.google.com/apikey | The tutorial is on: https://bit.ly/Axiom_AI \n")
        f.write("\nAPI = \n\n// WARNING: AFTER YOU ENTER THE API, PLEASE RESTART/REOPEN BETTERCMD OR ELSE YOUR AXIOM WILL NOT WORK!")

with open(AXIOM_FILE, "r") as f:
    lines = f.readlines()
    AXIOM_API = lines[3].strip().replace("API = ", "") if len(lines) > 3 else ""
# ---     
   
logging.basicConfig(
    filename="userfiles\\history.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
HISTORY_FILE = "userfiles\\history.log"

print("...") ; isNewUser = False # idk just put it here

DATETIME_ = datetime.now().strftime("%A, %d %B %Y  %H:%M:%S")
DATE_ = datetime.now().strftime("%A, %d %B %Y")
TIME_ = datetime.now().strftime("%H:%M:%S")

USER_FILE = "userfiles\\user.json"
CFUNCTIONS_FILE = "userfiles\\cfunc.json"
STARTUP_FILE = "userfiles\\.startup"
SETTINGS_FILE = "userfiles\\settings.json"
ROOT = os.path.join(os.getcwd(), 'userfiles')
dir_ = os.getcwd()

BTRCMD_COMMANDS = [
    "LOADBTRFILE", "BEEP", "BASE16", "BASE32", "BASE64", "BASE85", "NEO", "CH", "AXIOM", "DELAY", "ZIP", "UNZIP",
    "CF-LOADFUNC", "CF-RUNFUNC", "CF-HELP", "ABOUT",  "CLEAR", "ASKAXIOM", "NAVI", "IMG2ASCII", "CHANGEDIR",
    "DIRINFO", "HELP", "WHOAMI","CHANGEUSER", "CHANGEPW", "EXIT", "CLEARHISTORY", "IPINFO"
]

except_cmd = [
    "CD"
]

__version__ = "V1.0"
__author__ = "Delta Studios"

clear = lambda: os.system("cls" if os.name == "nt" else "clear")

LOG_LEVELS = {
    "debug": logging.debug,
    "info": logging.info,
    "warning": logging.warning,
    "error": logging.error,
    "critical": logging.critical
}

def debug_log(message: str, level: Literal["debug", "info", "warning", "error", "critical"]):
    log_func = LOG_LEVELS.get(level, logging.debug)  
    log_func(message)

# --- axiom ---
def letAxiomLearn(printLogo:bool=True) -> bool:
    global learned, chat
    
    if printLogo:
        printAxiomLogo()
    
    print("Please wait while Axiom is learning...")

    try:
        if AXIOM_API == "":
            raise ValueError("API key is missing! Please enter your API key in 'axiom.txt'.")

        ai.configure(api_key=AXIOM_API)
        model = ai.GenerativeModel()
        chat = model.start_chat()
        
        instructions = [
            "You are now Axiom, my personal AI assistant. You are intelligent, friendly, know coding, love technology, and are helpful.",
            "If someone asks 'Who are you?', ONLY answer: 'I am Axiom, a multimodal AI model developed by Google and enhanced by DeltaStudios. Ask me anything! :)'",
            "If someone asks 'What is BetterCMD?', ONLY answer: 'BetterCMD (btrCMD) is a powerful tool developed by DeltaStudios that enhances the Windows command prompt with additional useful features.'",
            f"If someone asks 'what date is today?', answer: {DATE_}",
            f"If someone asks 'what time is now?', answer: {TIME_} in AM/PM",
        ]
        
        for instruction in instructions:
            chat.send_message(instruction)
        
        learned = True
        print("Axiom has successfully learned!")
        return True

    except ValueError as e:  
        print(f"❌ {e}")
        return False
    except Exception as e:
        print(f"Unexpected error while initializing Axiom: {e}")
        return False

def printAxiomLogo():
    console.print("""
                ====================================================================================================================                                                                                                            
                [bold cyan]AAA                 [/][white]XXXXXXX       XXXXXXX     [bold cyan]IIIIIIIIII[/]          OOOOOOOOO          MMMMMMMM               MMMMMMMM
               [bold cyan]AdddA                [/][white]XdddddX       XdddddX     [bold cyan]IddddddddI[/]        OOdddddddddOO        MdddddddM             MdddddddM
              [bold cyan]AdddddA               [/][white]XdddddX       XdddddX     [bold cyan]IddddddddI[/]      OOdddddddddddddOO      MddddddddM           MddddddddM
             [bold cyan]AdddddddA              [/][white]XddddddX     XddddddX     [bold cyan]IIddddddII[/]     OdddddddOOOdddddddO     MdddddddddM         MdddddddddM
            [bold cyan]AdddddddddA             [/][white]XXXdddddX   XdddddXXX     [bold cyan]  IddddI  [/]     OddddddO   OddddddO     MddddddddddM       MddddddddddM
           [bold cyan]AdddddAdddddA            [/][white]   XdddddX XdddddX        [bold cyan]  IddddI  [/]     OdddddO     OdddddO     MdddddddddddM     MdddddddddddM
          [bold cyan]AdddddA AdddddA           [/][white]    XdddddXdddddX         [bold cyan]  Iddd:I  [/]     O:::::O     O:::::O     M:::::::M::::M   M::::M:::::::M
         [bold cyan]A:::::A   A:::::A          [/][white]     X:::::::::X          [bold cyan]  I::::I  [/]     O:::::O     O:::::O     M::::::M M::::M M::::M M::::::M
        [bold cyan]A:::::A     A:::::A         [/][white]     X:::::::::X          [bold cyan]  I::::I  [/]     O:::::O     O:::::O     M::::::M  M::::M::::M  M::::::M
       [bold cyan]A:::::AAAAAAAAA:::::A        [/][white]    X:::::X:::::X         [bold cyan]  I::::I  [/]     O:::::O     O:::::O     M::::::M   M:::::::M   M::::::M
      [bold cyan]A:::::::::::::::::::::A       [/][white]   X:::::X X:::::X        [bold cyan]  I::::I  [/]     O:::::O     O:::::O     M::::::M    M:::::M    M::::::M
     [bold cyan]A:::::AAAAAAAAAAAAA:::::A      [/][white]XXX:::::X   X:::::XXX     [bold cyan]  I::::I  [/]     O::::::O   O::::::O     M::::::M     MMMMM     M::::::M
    [bold cyan]A:::::A             A:::::A     [/][white]X::::::X     X::::::X     [bold cyan]II::::::II[/]     O:::::::OOO:::::::O     M::::::M               M::::::M
   [bold cyan]A:::::A               A:::::A    [/][white]X:::::X       X:::::X     [bold cyan]I::::::::I[/]      OO:::::::::::::OO      M::::::M               M::::::M
  [bold cyan]A:::::A                 A:::::A   [/][white]X:::::X       X:::::X     [bold cyan]I::::::::I[/]        OO:::::::::OO        M::::::M               M::::::M
 [bold cyan]AAAAAAA                   AAAAAAA  [/][white]XXXXXXX       XXXXXXX     [bold cyan]IIIIIIIIII[/]          OOOOOOOOO          MMMMMMMM               MMMMMMMM
====================================================================================================================================
                  """.replace("=", "[bold orange1]=[/]"), emoji=False)

learned = False
def askAxiom():
    if not learned:
        letAxiomLearn()
    
    def loading_effect(delay_:int|float=3):
        with console.status("[bold cyan]Axiom is thinking...[/]", spinner="dots"):
            time.sleep(delay_)
    
    clear()
    printAxiomLogo()
    def askprint_axiom():
        while True:
            question = input(f"🟢 You:  ")
            if (question.lower() == "quit") or (question.lower() == "exit"):
                loading_effect(0.4)
                console.print(f"🟣 Axiom: Goodbye!\n")
                break
            try:
                response = chat.send_message(question).text
                loading_effect()
                console.print(Markdown(f"\n🟣 Axiom:\n{response}\n"))
            except Exception as e:
                return f"⚠️ Error: {str(e)}"
        
    askprint_axiom()
    
def PromptaskAxiom(_prompt:str):
    if not learned:
        letAxiomLearn(False)
        
    def loading_effect(delay_:int=3):
        with console.status("[bold cyan]Axiom is thinking...[/]", spinner="dots"):
            time.sleep(delay_)
        print("\n")
        
    print(f"🟢 You: {_prompt}")
    try:
        response = chat.send_message(_prompt).text
        loading_effect()
        print(f"🟣 Axiom: {response}\n")
    except Exception as e:
        return f"⚠️ Error: {str(e)}"
# --- end of creating axiom ---

# --- navi ---
class NaVi(App):
    """Natrium Visual Improved"""

    def __init__(self, filename: str = "untitled.txt"):
        super().__init__()
        self.filename = filename
        self.text = [""]  
        self.cursor_x = 0  
        self.cursor_y = 0  
        self.scroll_offset = 0  
        self.modified = False  
        self.undo_stack = []  
        self.redo_stack = []  
        self.confirming_exit = False  

        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                self.text = f.read().splitlines() or [""]
    
    BINDINGS = [
        ("ESC", "quit", "Exit"),
        ("CTRL + S", "save", "Save"),
        ("CTRL + Z", "undo", "Undo"),
        ("CTRL + Y", "redo", "Redo"),
    ]
    
    def compose(self) -> ComposeResult:
        """Construct the layout."""
        yield Header(True)
        
        yield Vertical(
            Static(""), # empty line
            Static("", id="editor"),  # Text editor
        )
        
        yield Footer()

    def on_mount(self) -> None:
        """Called when the app starts."""
        self.update_screen()
        self.title = f"NaVi - Natrium Visual Improved @ {self.filename}"

    def on_key(self, event: Key) -> None:
        """Handle keyboard input."""
        try:
            if event.key == "escape":
                self.confirm_exit()
            elif event.key == "ctrl+s":
                self.save_file()
            elif event.key == "ctrl+z":
                self.undo()
            elif event.key == "ctrl+y":
                self.redo()
            elif event.key in ("up", "down", "left", "right"):
                self.move_cursor(event.key)
            elif event.key == "enter":
                self.move_cursor("enter")
            elif event.key == "backspace":
                self.delete_char()
            elif event.key == "delete":
                self.delete_char()
            elif len(event.character) == 1:
                self.insert_char(event.character)
        except TypeError: pass # best error handling ever
    
        self.update_screen()

    def move_cursor(self, direction: str) -> None:
        """Move the cursor correctly."""
        if direction == "up" and self.cursor_y > 0:
            self.cursor_y -= 1
        elif direction == "down":
            if self.cursor_y < len(self.text) - 1:
                self.cursor_y += 1
            else:
                self.text.append("")  # Add new line if none exists
                self.cursor_y += 1
        elif direction == "left":
            if self.cursor_x > 0:
                self.cursor_x -= 1
            elif self.cursor_y > 0:  # Move to the end of the previous line
                self.cursor_y -= 1
                self.cursor_x = len(self.text[self.cursor_y])
        elif direction == "right":
            if self.cursor_y < len(self.text) and self.cursor_x < len(self.text[self.cursor_y]):
                self.cursor_x += 1
            elif self.cursor_y < len(self.text) - 1:  # Move to the next line
                self.cursor_y += 1
                self.cursor_x = 0
        elif direction == "enter":
            if self.cursor_y < len(self.text) - 1 and not self.text[self.cursor_y].strip():
                self.text.insert(self.cursor_y + 1, "")
                self.cursor_y += 1  
            else:
                self.text.insert(self.cursor_y + 1, "")
                self.cursor_y += 1

        # Ensure the cursor doesn't exceed the line length
        self.cursor_x = min(self.cursor_x, len(self.text[self.cursor_y]))

        # Scrolling if the cursor exceeds the screen
        if self.cursor_y < self.scroll_offset:
            self.scroll_offset = self.cursor_y
        elif self.cursor_y >= self.scroll_offset + self.size.height:  
            self.scroll_offset = self.cursor_y - self.size.height

    def insert_char(self, char: str) -> None:
        """Insert character at the cursor position with auto-type, escape auto-close, and multi-line enter."""
        self.save_undo_state()

        pairs = {
            "(": ")", "{": "}", "[": "]", "\"": "\"", "'": "'", "<": ">"
        }

        line = self.text[self.cursor_y]

        if self.cursor_x < len(line) and line[self.cursor_x] == char and char in pairs.values():
            self.cursor_x += 1
            return

        if char in pairs:
            if self.cursor_x == len(line): 
                self.text[self.cursor_y] = line[:self.cursor_x] + char
            else:
                self.text[self.cursor_y] = line[:self.cursor_x] + char + pairs[char] + line[self.cursor_x:]
        else:
            self.text[self.cursor_y] = line[:self.cursor_x] + char + line[self.cursor_x:]

        self.cursor_x += 1
        self.modified = True

    def delete_char(self) -> None:
        """Delete character with Smart Backspace."""
        if self.cursor_x > 0:
            self.save_undo_state()
            line = self.text[self.cursor_y]

            pairs = {"(": ")", "{": "}", "[": "]", "\"": "\"", "'": "'", "<": ">"}
            if (
                self.cursor_x < len(line) - 1  
                and line[self.cursor_x - 1] in pairs
                and line[self.cursor_x] == pairs[line[self.cursor_x - 1]]
                and self.cursor_x - 1 == len(line) - 2  
            ):
                self.text[self.cursor_y] = line[:self.cursor_x - 1] + line[self.cursor_x + 1:]
                self.cursor_x -= 1
            else:
                self.text[self.cursor_y] = line[:self.cursor_x - 1] + line[self.cursor_x:]
                self.cursor_x -= 1

            self.modified = True
        elif self.cursor_y > 0: 
            self.save_undo_state()
            prev_line = self.text[self.cursor_y - 1]
            self.cursor_x = len(prev_line)
            self.text[self.cursor_y - 1] += self.text[self.cursor_y]
            del self.text[self.cursor_y]
            self.cursor_y -= 1
            self.modified = True

    def save_undo_state(self) -> None:
        """Save the current state for undo."""
        self.undo_stack.append((self.text[:], self.cursor_x, self.cursor_y))
        self.redo_stack.clear()  # Clear redo stack after a change

    def undo(self) -> None:
        """Revert to the last change."""
        if self.undo_stack:
            self.redo_stack.append((self.text[:], self.cursor_x, self.cursor_y))
            self.text, self.cursor_x, self.cursor_y = self.undo_stack.pop()
            self.modified = True

    def redo(self) -> None:
        """Revert to the change after undo."""
        if self.redo_stack:
            self.undo_stack.append((self.text[:], self.cursor_x, self.cursor_y))
            self.text, self.cursor_x, self.cursor_y = self.redo_stack.pop()
            self.modified = True

    def save_file(self) -> None:
        """Save the file."""
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                f.write("\n".join(self.text))
            self.modified = False
            self.notify(f"File '{self.filename}' saved successfully! \n{os.path.abspath(self.filename)}", severity="information")
        except Exception as e:
            self.notify(f"Failed to save file: {e}", severity="error")
    
    def confirm_exit(self) -> None:
        """Prompt for confirmation before exit if there are changes."""
        if not self.modified:
            self.exit()
        else:
            self.confirming_exit = True
            match msgbox.askyesnocancel("NaVi - Natrium Visual Improved", 
                                    "WARNING : File modified! Save?\n ~ Yes : Save and Exit \n ~ No : Exiting NaVi without saving \n ~ Cancel: Abort option"):
                case True:
                    self.notify(f"File has been saved as : {self.filename} in \n {os.path.abspath(self.filename)}")
                    self.save_file()
                    self.exit()
                case False:
                    self.exit()
                case None:
                    self.confirming_exit = False
                    self.update_screen()

    def update_screen(self) -> None:
        """Update the editor display."""
        text_display = Text()
        self.text_display = text_display
        visible_text = self.text[self.scroll_offset:self.scroll_offset + 26]  # Scrolled display

        for i, line in enumerate(visible_text, start=self.scroll_offset):
            if i == self.cursor_y:
                if len(line) == 0:
                    line_with_cursor = "|"
                else:
                    line_with_cursor = line[:self.cursor_x] + "|" + line[self.cursor_x:]
                text_display.append(f"[{i+1}] {line_with_cursor}\n", style="white")
            else:
                # text_display.append(f"[{i+1}] {line or '~'}\n", style="dim" if not line else "white")
                text_display.append(f"[~] {line}\n", style="dim" if not line else "white")

        self.query_one("#editor", Static).update(text_display)
# --- end of navi ---

# --- img2ascii ---
def img2ascii(path, width=100, chars=" .:-=+*#%@"):
    img = Image.open(path).convert("L")  # Convert to grayscale
    w, h = img.size
    aspect_ratio = h / w * 0.5  # Adjust for non-square pixels
    new_height = int(width * aspect_ratio)
    img = img.resize((width, new_height))

    pixels = np.array(img)
    ascii_chars = np.array(list(chars))
    scale_factor = 255 // (len(chars) - 1)

    ascii_img = "\n".join("".join(ascii_chars[p // scale_factor] for p in row) for row in pixels)
    print(ascii_img)
# ---

# --- get user's ip ---
def ipinfo(ip: str = None):
    try:
        # Ambil IP publik sendiri jika tidak ada input
        if ip is None:
            ip = requests.get("https://api64.ipify.org?format=json").json().get("ip")
        
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()

        if "bogon" in data:
            print("Invalid or private IP address.")
            return
        
        print(f"IP: {data.get('ip', 'Unknown')}")
        print(f"City: {data.get('city', 'Unknown')}")
        print(f"Region: {data.get('region', 'Unknown')}")
        print(f"Country: {data.get('country', 'Unknown')}")
        print(f"ISP: {data.get('org', 'Unknown')}")
        print(f"Location: {data.get('loc', 'Unknown')}")
        print(f"Timezone: {data.get('timezone', 'Unknown')}")

    except Exception as e:
        print(f"Error: {e}")
# ---

# --- zip / unzip ---
def zip_files(files: tuple, output: str = "output.zip", deleteOriginalFile: bool = False):
    try:
        with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zf:
            for file in files:
                if os.path.exists(file):
                    zf.write(file)
                    print(f"Added: {file}")
                else:
                    print(f"Warning: {file} not found!")

        print(f"Files successfully zipped into {output}")

        if deleteOriginalFile:
            for file in files:
                if os.path.exists(file):
                    os.remove(file)
                    print(f"Deleted: {file}")

    except Exception as e:
        print(f"Error: {e}")

def unzip_file(zip_path: str, extract_to: str = "output", deleteOriginalFile: bool = False):
    try:
        if not os.path.exists(zip_path):
            print(f"Error: {zip_path} not found!")
            return
        
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(extract_to)
            print(f"Files successfully extracted to {extract_to}")

        if deleteOriginalFile:
            os.remove(zip_path)
            print(f"Deleted: {zip_path}")

    except Exception as e:
        print(f"Error: {e}")
# ---

# --- window setting ---
def is_maximized():
    hwnd = win32gui.GetForegroundWindow()  
    return win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE) & win32con.WS_MAXIMIZE != 0

def is_fullscreen():
    hwnd = win32gui.GetForegroundWindow()
    screen_width = win32api.GetSystemMetrics(0) 
    screen_height = win32api.GetSystemMetrics(1)  
    rect = win32gui.GetWindowRect(hwnd) 

    return (rect[0] == 0 and rect[1] == 0 and 
            rect[2] == screen_width and rect[3] == screen_height)
    
def set_maximize():
    hwnd = win32gui.GetForegroundWindow() 
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE) 
    
def set_restore():
    hwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
# ---

# -- C-Function (custom function) ---
isCfunctionLoaded = False
def load_function() -> dict:
    global isCfunctionLoaded
    isCfunctionLoaded = False
    if not os.path.exists(CFUNCTIONS_FILE):
        print("No functions saved.")
        return {}
    
    with open(CFUNCTIONS_FILE, "r") as f:
        try:
            data = json.load(f)
            if not data:
                print("No functions saved.")
                return {}
            
            print("Loaded functions:")
            print("="*20)
            for func_name, func_info in data.items():
                print(f"Function Name: {func_name}")
                print(f"Type: {func_info['type']}")
                print(f"Function: {func_info['func']}")
                print("="*20)
            print("Run 'CF-RUNFUNC <func_name>' to run your customfunction")
                
            isCfunctionLoaded = True
            return data  
        except json.JSONDecodeError:
            print("Failed to load functions. The file might be corrupted.")
            return {}

def run_function(func_name: str) -> None:
    if not os.path.exists(CFUNCTIONS_FILE):
        print("No functions saved.")
        return
    
    if not isCfunctionLoaded:
        print("No functions loaded, try load the functions using 'CF-LOADFUNC'")
        return
    
    with open(CFUNCTIONS_FILE, "r") as f:
        try:
            data = json.load(f)
            func_info = data.get(func_name)
            if not func_info:
                print(f"Function '{func_name}' not found.")
                return
            
            if func_info['type'] == 'batch':
                os.system(func_info['func'])  
            elif func_info['type'] == 'python':
                exec(func_info['func']) 
            else:
                print("Unknown function type.")
        except json.JSONDecodeError:
            print("Failed to load functions. The file might be corrupted.")
# --- end of cfunc ---

def help_():
    print("=========== BetterCMD Root File's Usages ===========")
    seeRoot()
    print("\n=========== BetterCMD Help ===========")
    print("ABOUT          Information about BetterCMD")
    print("CLEAR          Clear the terminal screen")
    print("DIRINFO        Show current directory")
    print("HELP           Show this help message")
    print("CHANGEUSER     Change the user")
    print("CHANGEPW       Change the password")
    print("WHOAMI         See the current user")
    print("LOADBTRFILE    Load the BetterCMD (.btr) file and  run it in BetterCMD")
    print("BEEP           Play a beep with a set note, duration, volume")
    print("CH             Clears your command history")
    print("DELAY          Set a delay")
    print("AXIOM          Open chat with Axiom AI")
    print("ASKAXIOM       Asking Axiom AI with the specified prompt")
    print("NEO            Show system information")
    print("NAVI           Make/edit a file in a vim-like style")
    print("EXIT           Exit BetterCMD")
    print("CHANGEDIR      Changes the directory")
    print("\n=========== Tools ===========")
    print("IMG2ASCII      Convert image to an ascii")
    print("ZIP / UNZIP    Takes a folder path, and then convert it to .zip or unzip it")
    print("IPINFO         Get user's IP")
    print("\n=========== Encoding Commands ===========")
    print("BASE16         Encode/decode Base16")
    print("BASE32         Encode/decode Base32")
    print("BASE64         Encode/decode Base64")
    print("BASE85         Encode/decode Base85")
    print("\n=========== Custom Functions ===========")
    print("CF-LOADFUNC    Load your custom function")
    print("CF-RUNFUNC     Run your custom function")
    print("CF-HELP        Show Custom Function help")
    print("\n=========== CustomFunction Help ===========")
    print("CF-LOADFUNC    Load your custom function")
    print("CF-RUNFUNC     Run your custom function")
    print("CF-HELP        Open the CustomFunction's help")
    print("\n=========== Basic CMD Help ===========")
    os.system("help")

# --- base16 to base85 encode and decode ---
b16_encode = lambda obj: base64.b16encode(obj.encode()).decode()
b16_decode = lambda obj: base64.b16decode(obj.encode()).decode()

b32_encode = lambda obj: base64.b32encode(obj.encode()).decode()
b32_decode = lambda obj: base64.b32decode(obj.encode()).decode()

b64_encode = lambda obj: base64.b64encode(obj.encode()).decode()
b64_decode = lambda obj: base64.b64decode(obj.encode()).decode()

b85_encode = lambda obj: base64.b85encode(obj.encode()).decode()
b85_decode = lambda obj: base64.b85decode(obj.encode()).decode()
# ---

def playbeep(note: str, duration: float, volume: float, log: bool = True):
    """Create a beep sound"""
    frequencies = {
    "C1": 32.703, "C#1": 34.648, "D1": 36.708, "D#1": 38.891, "E1": 41.203, "F1": 43.654, "F#1": 46.249, "G1": 49.000, "G#1": 51.913, "A1": 55.000, "A#1": 58.270, "B1": 61.735,
    "C2": 65.406, "C#2": 69.296, "D2": 73.416, "D#2": 77.782, "E2": 82.407, "F2": 87.307, "F#2": 92.499, "G2": 98.000, "G#2": 103.826, "A2": 110.000, "A#2": 116.541, "B2": 123.471,
    "C3": 130.813, "C#3": 138.591, "D3": 146.832, "D#3": 155.563, "E3": 164.814, "F3": 174.614, "F#3": 184.997, "G3": 195.998, "G#3": 207.652, "A3": 220.000, "A#3": 233.082, "B3": 246.942,
    "C4": 261.626, "C#4": 277.183, "D4": 293.665, "D#4": 311.127, "E4": 329.628, "F4": 349.228, "F#4": 369.994, "G4": 392.000, "G#4": 415.305, "A4": 440.000, "A#4": 466.164, "B4": 493.883,
    "C5": 523.251, "C#5": 554.365, "D5": 587.330, "D#5": 622.254, "E5": 659.255, "F5": 698.456, "F#5": 739.989, "G5": 783.991, "G#5": 830.609, "A5": 880.000, "A#5": 932.328, "B5": 987.767,
    "C6": 1046.502, "C#6": 1108.731, "D6": 1174.659, "D#6": 1244.508, "E6": 1318.510, "F6": 1396.913, "F#6": 1479.978, "G6": 1567.982, "G#6": 1661.219, "A6": 1760.000, "A#6": 1864.655, "B6": 1975.533,
    "C7": 2093.005, "C#7": 2217.461, "D7": 2349.318, "D#7": 2489.016, "E7": 2637.020, "F7": 2793.826, "F#7": 2959.955, "G7": 3135.964, "G#7": 3322.438, "A7": 3520.000, "A#7": 3729.310, "B7": 3951.067,
    "C8": 4186.009
    }
    
    if note in frequencies:
        frequency = frequencies[note]
        sample_rate = 44100  
        duration_samples = int(sample_rate * duration)
        t = np.linspace(0, duration, duration_samples, False)
        signal = volume * np.sin(2 * np.pi * frequency * t)  

        p = pyaudio.PyAudio()
        if log:
            console.print(f"[cyan]Played note: [/][bold blue]{note}[/][cyan] with frequency[/]: [bold blue]{frequency}[/][cyan] volume: [bold blue]{volume}[/]")
        stream = p.open(rate=sample_rate, channels=1, format=pyaudio.paFloat32, output=True)
        stream.write(signal.astype(np.float32).tobytes())
        stream.stop_stream()
        stream.close()
        p.terminate()

def loadbtrfile(path: str, user: str):
    if not os.path.exists(path):
        print(f"❌ Error: File '{path}' not found. Please check the file path.")
        return 

    try:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith(("//", "#", ":")):  
                    continue
                if morecmd(line, user):
                    continue
                exit_code = os.system(line)
                if exit_code != 0:
                    print(f"⚠️ Warning: Command '{line}' failed with exit code {exit_code}.")
        
        print("\n✅ File processed successfully.")

    except Exception as e:
        print(f"❌ Unexpected error while processing '{path}': {e}")

def completer(text, state):
    commands = BTRCMD_COMMANDS
    options = [cmd for cmd in commands if cmd.startswith(text.upper())]
    return options[state] if state < len(options) else None

def neo():
    import psutil, GPUtil
    
    # --- cpu info stuff ---
    def get_cpu_info():
        try:
            cpu_info = subprocess.check_output(
                "powershell -Command \"(Get-CimInstance Win32_Processor).Name\"", shell=True
            ).decode().strip()
            core_count = psutil.cpu_count(logical=True)
            freq = psutil.cpu_freq()
            cpu_freq = f"{freq.current / 1000:.3f}GHz" if freq else "Unknown GHz"
            return f"{cpu_info} ({core_count}) @ {cpu_freq}"
        except Exception:
            return "Unknown"

    system_info: dict[str, str] = {
        "Operating System": platform.system(),
        "OS Version": platform.version(),
        "Architecture": platform.architecture()[0],
        # "CPU": f"{platform.processor()} @ {psutil.cpu_freq().current / 1000:.2f}GHz",
        "CPU": get_cpu_info(),
        "BetterCMD Version": __version__,
        "Platform": sys.platform,
        "WindowsName": platform.node(),
        "GPUs": ", ".join(gpu.name for gpu in GPUtil.getGPUs()),
        "Storage": [psutil.disk_usage('/').total / (1024**3), psutil.disk_usage('/').used / (1024**3)]
    }
    
    console.print(fr"""
 [white]//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\\
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\\
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++   [bright_red]{user}[#FFA500]@[/#FFA500]{system_info["WindowsName"]}[/]
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++   -{"-"*len(system_info["WindowsName"])}{"-"*len(user)}
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&   [#e54ef2]OS [/][#FFA500]: [/]{system_info['Operating System']}
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&   [#e54ef2]OS Version[/][#FFA500] : [/]{system_info["OS Version"]}
&&&&&&&&&&&&&&&&+++&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&   [#e54ef2]Architecture[/][#FFA500] : [/]{system_info["Architecture"]}
&&&&&&&&&&&$*!:::::::!%&&&&&&&&&$:!+&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&   [#e54ef2]Platform[/][#FFA500] : [/]{system_info['Platform']}
&&&&&&&&&$:.:*%$++$$%!%&&&&&&&&&&!.!&&&&&&&&&&&&&[#FFA500]@@[/]&&&&&&&&&&&&&&&&[#FFA500]@@[/]&&&&&&&&&&&&&&&   [#e54ef2]CPU[/][#FFA500] : [/]{system_info['CPU']}
&&&&&&&&*..%&&&&&&&&&&&&&&&++&&&&+:.%&&&&&&&&&&&&[#FFA500]%%[/]+&&&&&&&&&&&&&&&[#FFA500]%%[/]+&&&&&&&&&&&&&&   [#e54ef2]GPU[/][#FFA500] : [/]{system_info["GPUs"]}
&&&&&&&%..%&&&&&&&&&&&&&&&*..*&&&&$.:+&&&&&&&&&&&[#FFA500]%%[/]+&&&&&&&&&&&&&&&[#FFA500]%%[/]+&&&&&&&&&&&&&&   [#e54ef2]Storage[/][#FFA500] : [/]{system_info['Storage'][1]:.2f}/{system_info['Storage'][0]:.2f} GB
&&&&&&&:.!&&&&&&&&&&&&&&&&%::*&&&&&*.!&&&&&&&&&&&[#FFA500]%%[/]+&&&&&&&&&&&&&&&[#FFA500]%%[/]+&&&&&&&&&&&&&&   [#e54ef2]BetterCMD Version[/][#FFA500] : [/]{system_info['BetterCMD Version']}
&&&&&&+..%&&&&&&&&&&&&&&&&&++&&&&&&+:.%&&&[#FFA500]%%%%%%%%%%%%%%%%[/]&&[#FFA500]%%%%%%%%%%%%%%%%[/]&&&&&&&&
&&&&&&$..%&&&&&&&&&&&&&&&&&&&&&&&&&&$.:+&&&++++++[#FFA500]%%[/]$+++++&&&+++++++[#FFA500]%%[/]$+++++&&&&&&&&&
&&&&&&+:.!&&&&&&&&&&&&&&&&&&&&&&&&&&&*.!&&&&&&&&&[#FFA500]%%[/]+&&&&&&&&&&&&&&[#FFA500]%%[/]+&&&&&&&&&&&&&&&
&&&&&&&*.:$&&&&&&&&&&&&&&&&&&&&&&&&&&&:.%&&&&&&&&[#FFA500]%%[/]+&&&&&&&&&&&&&&[#FFA500]%%[/]+&&&&&&&&&&&&&&&
&&&&&&&+!.:$&&&&&&&&&&&&&&&&&&&&&&&&&&$.:+&&&&&&&[#FFA500]@@[/]+&&&&&&&&&&&&&&[#FFA500]@@[/]+&&&&&&&&&&&&&&&
&&&&&&&&&*..!%$+++++$%+&&&%::%&&&&&&&&&*.!&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
&&&&&&&&&&+%!:::::::::+&&&*..*&&&&&&&&&&!:%&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
&&&&&&&&&&&&&&++++++&&&&&&&++&&&&&&&&&&&&&&[blue]==================[/]&&&&&&&&&&&&&&&&&&&&&&&
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
\\&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&//
 \\&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&//
""")

def about_():
    console.print("[bright_magenta]BetterCMD [/][#FFA500]([/][sky_blue1]btrCMD[/][#FFA500])[/] is a program made from [cyan]DeltaStudios[/] that add usefull feature that normal Windows command prompt doesn't have.")
    console.print("[bright_red]License[/] [#FFA500]:[/] [bright_red]LICENSE.txt[/] [#FFA500]|[/] [blue]More Info[/] [#FFA500]:[/] [blue]README.txt and at[/] [cyan]BetterCMD's[/] [link=https://github.com/DeltaStudios01/BetterCMD]GitHub Repos[/link]")
    return True

# --- connect/pipe ---
def connect(first_func, second_func, *args):
    return second_func(first_func, *args)
# ---

# main function (adding more commands)
def morecmd(cmd: str, user: str) -> bool:
    if cmd.lower().startswith("cd"):
        print("Due to BetterCMD Safe Directory Restrictions, please use 'changedir' instead.")
        return True
    
    if cmd.lower().startswith("changedir"):
        try:
            global dir_
            os.chdir(cmd.split("changedir ", 1)[1])
            dir_ = os.getcwd()
            return True
        except:
            print("Usage: changedir <dir_location>")
            print("<> = Required")
    
    if cmd.lower().startswith("zip"):
        parts = cmd.split()

        if len(parts) < 2:
            print("Usage: zip [-d] <file1> <file2> ... <fileN>")
            print("<> = Required, [] = Optional, -d = Delete Original File")
            return True

        deleteOriginalFile = "-d" in parts
        files = [p for p in parts[1:] if p != "-d"]

        if not files:
            print("Error: No files provided!")
            return True

        zip_files(tuple(files), "output.zip", deleteOriginalFile)
        return True

    if cmd.lower().startswith("unzip"):
        parts = cmd.split()

        if len(parts) < 2:
            print("Usage: unzip <zip_file> [extract_to] [-d]")
            print("<> = Required, [] = Optional, -d = Delete Original File")
            return True

        zip_file = parts[1].strip('"')
        extract_to = parts[2].strip('"') if len(parts) > 2 and parts[2] != "-d" else "output"
        deleteOriginalFile = "-d" in parts

        unzip_file(zip_file, extract_to, deleteOriginalFile)
        return True
    
    if cmd.lower().startswith("ipinfo"):
        parts = cmd.split(" ")
        
        if len(parts) <= 1:
            print("Usage: ipinfo <ip>")
            print('<> = Required | If you want your ip info fill <ip> as "self"')
            return True
            
        ip = parts[1]
        if ip.lower() in ["me", "self"]:
            ipinfo()
        else:
            ipinfo(ip)
    
    if cmd.lower().startswith("img2ascii"):
        parts = cmd.split(" ", 2)
        
        if len(parts) <= 2:
            print("Usage: img2ascii <size> <image_path")
            print("<> = Required")
            return True
        
        path = parts[2].strip()
        size = parts[1]
        img2ascii(path, int(size))
    
    if cmd.lower().startswith("navi"):
        parts = cmd.split(" ", 1)
        
        if len(parts) < 2:
            print("Usage: navi <FileOrFilePath>")
            print("<> = Required")
            return True
        
        NaVi(parts[1]).run()
        
    if cmd.lower().startswith("delay"):
        parts = cmd.split(" ", 1)
        
        if len(parts) <= 1:
            print("Usage: delay <seconds>")
            print("<> = Required")
            return True
        
        delay(int(parts[1]))
        return True

    if cmd.lower() == "axiom":
        askAxiom()
        
    if cmd.lower().startswith("askaxiom"):
        parts = cmd.strip().split(" ", 1)
        
        if len(parts) <= 1:
            print("Usage: askaxiom <prompt>")
            print("<> = Required")
            return True
        
        prompt = parts[1]
        PromptaskAxiom(prompt)
    
    if (cmd.lower() == "clearhistory") or (cmd.lower() == "ch"):
        with open(HISTORY_FILE, "r+") as f:
            f.truncate(0)
            print("History's Cleared")
        return True
    
    if cmd.lower().startswith("$"):
        parts = cmd.split("->", 1)
        
        if len(parts) < 2:
            print("Usage: $<var_name> -> <var_content>")
            print("<> = Required")
            return True

        var_name = parts[0].strip().replace("$", "")
        var_content = parts[1].strip()  
        result = subprocess.run(f"setx {var_name} \"{var_content}\"", shell=True, capture_output=True, text=True)
        output = result.stdout.strip()  

        cleaned_output = output.replace("SUCCESS: Specified value was saved.", "").strip()
        
        os.environ[var_name] = var_content  
        os.system(f"set {var_name}={var_content}") 
    
        if cleaned_output:
            print(cleaned_output)
            
        return True
 
    if cmd.lower() == "neo":
        neo()
        return True

    if (cmd.lower() == "whoami") or ((cmd.lower() == "whotheheckami")):
        print(user)
        return True
    
    if cmd.strip().lower().startswith("loadbtrfile"):
        parts = cmd.split(" ", 1)  
        if len(parts) < 2:
            print("Usage: loadbtrfile <path>")
            return True
        path = parts[1].strip()
        loadbtrfile(path, user) 
        return True
    
    if cmd.lower().startswith("beep"):
        notes = [
        "C1", "C#1", "D1", "D#1", "E1", "F1", "F#1", "G1", "G#1", "A1", "A#1", "B1",
        "C2", "C#2", "D2", "D#2", "E2", "F2", "F#2", "G2", "G#2", "A2", "A#2", "B2",
        "C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3", "B3",
        "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4",
        "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", "B5",
        "C6", "C#6", "D6", "D#6", "E6", "F6", "F#6", "G6", "G#6", "A6", "A#6", "B6",
        "C7", "C#7", "D7", "D#7", "E7", "F7", "F#7", "G7", "G#7", "A7", "A#7", "B7",
        "C8"]
        parts = cmd.split(" ")
        if len(parts) < 4:
            print("Usage: beep <note> <duration> <volume> [-log]")
            print("[] = Optional, <> = Required, -log = If used, the note log will be activated; If not, the note log will not be activated")
            return True
        note = parts[1].strip('"').upper()
        dur = float(parts[2].lower())
        vol = float(parts[3].lower())
        try:
            log = parts[4].lower()
        except IndexError: 
            log = ""

        _log = log == "-log" 
        
        if note not in notes:
            console.print(f"[bold red]ERROR: Invalid note![/]; valid note: {notes}")
            return False
        
        playbeep(note, dur, vol, _log)
        return True
    
    if cmd.lower().startswith("base16"):
        parts = cmd.split(" ")
        if len(parts) < 3:
            print("Usage: base16 <data> -e/-d")
            print("[] = Optional, <> = Required, -e = Encrypt, -d = Decrypt")
            return True
        data = parts[1].strip('"')
        option = parts[2].lower()
        
        if option == "-e":
            print(f"Encoded (Base16): {b16_encode(data)}")
        elif option == "-d":
            print(f"Decoded (Base16): {b16_decode(data)}")
        else:
            print("Invalid option. Use -e (encode) or -d (decode).")
        return True
    
    elif cmd.lower().startswith("base32"):
        parts = cmd.split(" ")
        if len(parts) < 3:
            print("Usage: base32 <data> -e/-d")
            print("[] = Optional, <> = Required, -e = Encrypt, -d = Decrypt")
            return True
        data = parts[1].strip('"')
        option = parts[2].lower()
        
        if option == "-e":
            print(f"Encoded (Base32): {b32_encode(data)}")
        elif option == "-d":
            print(f"Decoded (Base32): {b32_decode(data)}")
        else:
            print("Invalid option. Use -e (encode) or -d (decode).")
        return True
    
    elif cmd.lower().startswith("base64"):
        parts = cmd.split(" ")
        if len(parts) < 3:
            print("Usage: base64 <data> -e/-d")
            print("[] = Optional, <> = Required, -e = Encrypt, -d = Decrypt")
            return True
        data = parts[1].strip('"')
        option = parts[2].lower()
        
        if option == "-e":
            print(f"Encoded (Base64): {b64_encode(data)}")
        elif option == "-d":
            print(f"Decoded (Base64): {b64_decode(data)}")
        else:
            print("Invalid option. Use -e (encode) or -d (decode).")
        return True
    
    elif cmd.lower().startswith("base85"):
        parts = cmd.split(" ")
        if len(parts) < 3:
            print("Usage: base85 <data> -e/-d")
            print("[] = Optional, <> = Required, -e = Encrypt, -d = Decrypt")
            return True
        data = parts[1].strip('"')
        option = parts[2].lower()
        
        if option == "-e":
            print(f"Encoded (Base85): {b85_encode(data)}")
        elif option == "-d":
            print(f"Decoded (Base85): {b85_decode(data)}")
        else:
            print("Invalid option. Use -e (encode) or -d (decode).")
        return True
    
    if cmd.lower() == "cf-loadfunc":
        load_function()  
        return True
    elif cmd.lower().startswith("cf-runfunc"):
        func_name = cmd.split(" ")[1] if len(cmd.split(" ")) > 1 else ""
        if func_name:
            run_function(func_name) 
        else:
            print("Usage: cf-runfunc <file_path>")
            print("[] = Optional, <> = Required")
        return True
    elif cmd.lower() == "cf-help":
        print("============= CustomFunction Help =============")
        print("CF-LOADFUNC | Usage: cf-loadfunc | Load your customfunction")
        print("CF-RUNFUNC  | Usage: cf-runfunc <your function's name> | Run your customfunction")
        print("==== How To Create Your Own CustomFunction ====")
        print(f"1. Open directory: {os.path.join(os.getcwd(), 'userfiles')}")
        print("2. Open the 'cfunc.json' file.")
        print("3. Add your custom function in the file using this template:")
        print("""
        {
            "test1": { <- This is the name of your function
                "func": "print(\"Hello, world\")", 
                "type": "python"
            },
            "test2": {
                "func": "echo \"Hello, world\"", <- This is the function executed
                "type": "batch" <- This is the type of your function (acceptables: "batch" or "python")
            }
        }
        """)
        print("4. Save the file.")
        print("5. Test it using cf-runfunc <your_func_name>")
        print("==== Rules for CustomFunction ====")
        print("1. The 'func' key contains the actual code to execute.")
        print("2. The 'type' key specifies the function type ('python' or 'batch').")
        print("3. Make sure the name of your function is without space (using underscore).")
        print("4. Make sure your JSON syntax is valid.")
        print("5. Only add functions you trust to avoid security risks.")
        return True
    
    if cmd.lower() == "about":
        about_()
    elif cmd.lower() == "clear":
        clear()
        return True
    elif cmd.lower() == "dirinfo":
        print(f"Current Directory: {os.getcwd()}")
        return True
    elif cmd.lower() == "help":
        help_()
        return True
    elif cmd.lower() == "changeuser":
        change_user(user)
        return True
    elif cmd.lower() == "changepw":
        change_password(user)
        return True
    return False

# user thing
def load_user():
    if not os.path.exists(USER_FILE):
        return None, None
    with open(USER_FILE, "r") as f:
        try:
            data = json.load(f)
            return b85_decode(data.get("user")), b85_decode(data.get("password"))
        except json.JSONDecodeError:
            return None, None

# def save_func(func_name: str, func: str, _type: str) -> None:
#     with open(CFUNCTIONS_FILE, "w") as f:
#         json.dump({func_name: {"func": func, "type": _type}}, f, indent=4)

def save_user(user: str, pw: str) -> None:
    with open(USER_FILE, "w") as f:
        # making the user and the password encoded
        json.dump({"user": b85_encode(user), "password": b85_encode(pw), "date_created" : DATE_}, f, indent=4)
        print("Created user.json")

def sign_up(*, forTesting: bool = False) -> str:
    global isNewUser
    if not forTesting:
        user = input("Create a username: ").strip()
    else:
        user = "TestUser0"
    if not user: user = "User0" ; print("Username given was empty, default user is: " + user)
    if not forTesting:
        pw = input("Create a password (press Enter to leave it empty): ").strip()
    else:
        pw = "usr1234testing"
    save_user(user, pw)
    print(f"Account created for {user}!")

    with open(CFUNCTIONS_FILE, "w") as f:
        json.dump({"example1": {"func": "print(\"Hello, world\")", "type": "python"}, "Example2": {"func": "echo \"Hello, world\"", "type": "batch"}}, f, indent=4)
        print("Created cfunc.json!")
        
    if forTesting:
        with open("userfiles\\usertest.txt", "w") as f:
            f.write(f"User: {user}\nPassword: {pw}")
            print("Created usertest.txt!")
    
    print("Created history.log!")
    print("Created .startup!")
    delay(1)
    clear()
    
    isNewUser = True
    return user

def ask_password(expected_pw: str) -> bool:
    entered_password = input("Please enter the password to continue: ").strip()
    
    if entered_password == expected_pw:
        clear()
        return True
    else:
        clear()
        print("Incorrect password. Command aborted.")
        return False

def checkcmd(cmd: str) -> bool:
    dangerous_keywords = ["del", "format", "erase", "rm", "shutdown", "rd", "rmdir"]
    for keyword in dangerous_keywords:
        if keyword in cmd.lower():
            return True
    return False

def change_user() -> None:
    new_user = input("Enter your new username: ").strip()
    pw = input("Enter your current password to confirm: ").strip()
    _, stored_pw = load_user()
    if pw == stored_pw:
        save_user(new_user, stored_pw)
        print(f"Username changed successfully to {new_user}!")
    else:
        print("Password incorrect. Username not changed.")

def change_password(user: str) -> None:
    old_pw = input("Enter your current password: ").strip()
    _, stored_pw = load_user()
    if old_pw == stored_pw:
        new_pw = input("Enter your new password: ").strip()
        save_user(user, new_pw)
        print("Password changed successfully!")
    else:
        print("Current password incorrect. Password not changed.")

NoWelcomeSign = None # Settings
IgnoreStartup = None # Settings

def startupcommands():
    global NoWelcomeSign, IgnoreStartup
    if not os.path.exists(STARTUP_FILE):
        with open(STARTUP_FILE, "w+") as f:
            f.write("// Startup commands, you can run BetterCMD or Normal CMD here when you open the BetterCMD.\n\n// Settings: \n// --NOWELCOMESIGN <true/false> : Turn on/off the welcome sign [default: false]\n// --STARTUP <true/false> : Activate/Disable startup commands [default: true]\n\n")
    with open(STARTUP_FILE, "r") as f:
        for cmd in f:
            cmd = cmd.strip()
            
            if not cmd or cmd.startswith(("//", "#", ":")): 
                continue
            
            if cmd.upper().startswith("--NOWELCOMESIGN TRUE"):
                NoWelcomeSign = True
            elif cmd.upper().startswith("--NOWELCOMESIGN FALSE"):
                NoWelcomeSign = False
            elif cmd.upper().startswith("--STARTUP TRUE"):
                IgnoreStartup = True
            elif cmd.upper().startswith("--STARTUP FALSE"):
                IgnoreStartup = False
                
            elif any(cmd.upper().startswith(command) for command in BTRCMD_COMMANDS):
                morecmd(cmd, user)
            else:
                os.system(cmd)
                
            if IgnoreStartup:
                clear()

def seeRoot():
    console.print(f"""[bright_blue]userfiles[/] [#FFA500]@[/] [cyan]{ROOT}[/]
[bright_blue]├──[/][sky_blue1][  .startup   ] [/][#FFA500]|[/] File that runs every time BetterCMD is opened 
[bright_blue]├──[/][sky_blue1][  axiom.txt  ] [/][#FFA500]|[/] Google Gemini API key storage for AXIOM in BetterCMD
[bright_blue]├──[/][sky_blue1][ cfunc.json  ] [/][#FFA500]|[/] File that create your own functions that can be runned in BetterCMD
[bright_blue]├──[/][sky_blue1][ history.log ] [/][#FFA500]|[/] File that have your command history
[bright_blue]└──[/][sky_blue1][  user.json  ] [/][#FFA500]|[/] User's file that contain secured username, secured password, and date created""")

# main function (for user interface and handle all commands)
def main(user: str) -> None:
    # auto complete
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)
    
    if not NoWelcomeSign:
        console.print(Panel(f"Hello, {user}! Today's date is {DATETIME_}", title="BetterCMD", border_style="cyan"))
    _, pw = load_user()
    if isNewUser:
        help_()
    while True:
        try:
            console.print(f"[cyan]┌─ {dir_} [#FFA500]@ [cyan]{user}")    
            console.print( "[cyan]└─[#FFA500]>> ", end="")  
            cmd = input().strip() # user input 
            debug_log(f"Executing command: {cmd}", "info")
            if cmd.lower() == "exit":
                print("Exiting the BetterCMD. Goodbye!")
                delay(1)
                if is_fullscreen() or is_maximized():
                    set_restore()
                clear()
                break
            elif any(cmd.upper().startswith(command) for command in BTRCMD_COMMANDS) \
                or any(cmd.upper().startswith(command) for command in except_cmd):
                morecmd(cmd, user)
            elif checkcmd(cmd):
                if not ask_password(pw):
                    continue  
            elif not any(cmd.upper().startswith(command) for command in BTRCMD_COMMANDS):
                os.system(cmd)
            else:
                print(f"Error: Function '{cmd}' was not found")
                debug_log("Function not found", "warning")
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt detected. Type 'exit' to quit.")
            debug_log("KeyBoardInterrupt", "warning")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            debug_log(e, "error")
            
#* ---------------------------------------------------------- RUN THE PROGRAM ----------------------------------------------------------
if __name__ == "__main__":
    if not (is_maximized() or is_fullscreen()):
        console.print(f"\n[bold yellow]{"="*100}")
        console.print("[bold red]WARNING: It is recommended to run BetterCMD in Fullscreen or Maximized mode for the best experience.")
        console.print(f"[bold yellow]{"="*100}")
        
        choice = input("Would you like to maximize BetterCMD now? (Y/n): ").strip().lower()
        if choice in ["", "y", "yes"]:
            set_maximize()
        else:
            console.print("[cyan]Continuing with the current window size...[/]")
            delay(1)
    
    clear()
    user, pw = load_user()
    if not user: # creating user if first time using BetterCMD
        console.print(Panel("Hello! Welcome to BetterCMD, let's get you started!", title="BetterCMD", border_style="cyan"))
        delay(1)
        
        user = sign_up()
    if not IgnoreStartup:
        startupcommands()
    
    main(user)