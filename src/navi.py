# ./src/navi.py

from textual.app import App, ComposeResult
from textual.widgets import Static, Footer, Header
from textual.containers import Vertical
from textual.events import Key
from rich.text import Text
from tkinter import messagebox as msgbox
from textual.events import Key
import os

class NaVi(App):
    """Natrium Visual Improved"""

    def __init__(self, filename:str = "untitled.txt"):
        super().__init__()
        self.text = [""]  # Text buffer
        self.cursor_x = 0  # Cursor position (column)
        self.cursor_y = 0  # Cursor position (row)
        self.filename = filename  # Default file name
        self.scroll_offset = 0  # For scrolling
        self.modified = False  # To track if there are changes
        self.undo_stack = []  # Undo stack
        self.redo_stack = []  # Redo stack
        self.confirming_exit = False  # Exit confirmation mode
    
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
            self.insert_char("\n") 
        elif event.key == "backspace":
            self.delete_char()
        elif event.key == "delete":
            self.delete_char()
        elif len(event.character) == 1:
            self.insert_char(event.character)

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
            if self.cursor_y < len(self.text) - 1:
                self.cursor_y += 1
            else:
                self.text.append("")  # Add new line if none exists
                self.cursor_y += 1

        # Ensure the cursor doesn't exceed the line length
        self.cursor_x = min(self.cursor_x, len(self.text[self.cursor_y]))

        # Scrolling if the cursor exceeds the screen
        if self.cursor_y < self.scroll_offset:
            self.scroll_offset = self.cursor_y
        elif self.cursor_y >= self.scroll_offset + 26:  # Displaying 26 lines on screen
            self.scroll_offset = self.cursor_y - 25

    def insert_char(self, char: str) -> None:
        """Insert character at the cursor position with auto-type, escape auto-close, and multi-line enter."""
        self.save_undo_state()

        pairs = {
            "(": ")",
            "{": "}",
            "[": "]",
            "\"": "\"",
            "'": "'",
            "<": ">"
        }

        line = self.text[self.cursor_y]

        # Handle Enter in the middle of a line
        if char == "\n":
            new_line = line[self.cursor_x:]  # Teks setelah kursor pindah ke baris baru
            self.text[self.cursor_y] = line[:self.cursor_x]  # Simpan teks sebelum kursor
            self.text.insert(self.cursor_y + 1, new_line)  # Tambahkan baris baru di bawahnya
            self.cursor_y += 1
            self.cursor_x = 0
            self.modified = True
            return

        # Escape auto-close (if next char is the closing pair, just move cursor)
        if self.cursor_x < len(line) and line[self.cursor_x] == char and char in pairs.values():
            self.cursor_x += 1
            return

        # Auto-type for pairs
        if char in pairs:
            self.text[self.cursor_y] = line[:self.cursor_x] + char + pairs[char] + line[self.cursor_x:]
        else:
            self.text[self.cursor_y] = line[:self.cursor_x] + char + line[self.cursor_x:]

        self.cursor_x += 1
        self.modified = True


    def delete_char(self) -> None:
        """Delete character or merge lines with Smart Backspace."""
        if self.cursor_x > 0:
            self.save_undo_state()
            line = self.text[self.cursor_y]

            # Smart Backspace: Remove both pairs if they're empty
            pairs = {"(": ")", "{": "}", "[": "]", "\"": "\"", "'": "'", "<": ">"}
            if self.cursor_x < len(line) and line[self.cursor_x - 1] in pairs and line[self.cursor_x] == pairs[line[self.cursor_x - 1]]:
                self.text[self.cursor_y] = line[:self.cursor_x - 1] + line[self.cursor_x + 1:]
                self.cursor_x -= 1
            else:
                self.text[self.cursor_y] = line[:self.cursor_x - 1] + line[self.cursor_x:]
                self.cursor_x -= 1

            self.modified = True
        elif self.cursor_y > 0:  # Merge with the previous line
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
            with open(self.filename, "w") as f:
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

if __name__ == "__main__":
    filepath = input("Please input the file/filepath here: ")
    NaVi(filepath).run()