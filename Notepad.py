import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import tkinter.font as tkFont
import os, sys

# Initialize root window
root = tk.Tk()
root.title("Untitled - Notepad")
root.geometry("800x600")

# Font setup
current_font = tkFont.Font(family="Consolas", size=12)

# Text widget
text_area = tk.Text(root, undo=True, font=current_font)
text_area.pack(fill=tk.BOTH, expand=1)

# Track file path and save state
current_file = None
is_saved = True

# --- Title Update ---
def update_title():
    prefix = "" if is_saved else "*"
    name = os.path.basename(current_file) if current_file else "Untitled"
    root.title(f"{prefix}{name} - Notepad")

# --- Menu Functions ---
def new_file(event=None):
    global current_file, is_saved
    if not confirm_discard_changes():
        return
    text_area.delete(1.0, tk.END)
    current_file = None
    is_saved = True
    update_title()

def open_file(event=None):
    global current_file, is_saved
    if not confirm_discard_changes():
        return
    file_path = filedialog.askopenfilename(filetypes=[
        ("Text Files", "*.txt"),
        ("Python Files", "*.py"),
        ("C Files", "*.c"),
        ("HTML Files", "*.html"),
        ("Batch Files", "*.bat"),
        ("Log Files", "*.log"),
        ("All Files", "*.*")
    ])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, content)
        current_file = file_path
        is_saved = True
        update_title()

def save_file(event=None):
    global current_file, is_saved
    if not current_file:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                  filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            current_file = file_path
    if current_file:
        with open(current_file, "w", encoding="utf-8") as file:
            file.write(text_area.get(1.0, tk.END))
        is_saved = True
        update_title()

def exit_app():
    if not is_saved:
        name = os.path.basename(current_file) if current_file else "Untitled"
        response = messagebox.askyesnocancel("Notepad", f"Do you want to save changes to {name}?")
        if response:  # Yes
            save_file()
            root.destroy()
        elif response is False:  # No
            root.destroy()
        else:  # Cancel
            return
    else:
        root.destroy()

def confirm_discard_changes():
    if not is_saved:
        name = os.path.basename(current_file) if current_file else "Untitled"
        response = messagebox.askyesnocancel("Notepad", f"Do you want to save changes to {name}?")
        if response:  # Yes
            save_file()
            return True
        elif response is False:  # No
            return True
        else:  # Cancel
            return False
    return True

def copy_text():
    text_area.event_generate("<<Copy>>")

def paste_text():
    text_area.event_generate("<<Paste>>")

def select_all():
    text_area.tag_add("sel", "1.0", "end")

def change_font_size():
    new_size = simpledialog.askinteger("Font Size", "Enter new font size:", minvalue=8, maxvalue=72)
    if new_size:
        current_font.configure(size=new_size)

def show_about():
    messagebox.showinfo("About", "Notepad created by Tejas.")

# --- Detect Unsaved Changes ---
def on_modified(event=None):
    global is_saved
    if is_saved:
        is_saved = False
        update_title()
    text_area.edit_modified(False)

text_area.bind("<<Modified>>", on_modified)

# --- Menu Bar ---
menu_bar = tk.Menu(root)

# File Menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file, accelerator="Ctrl+N")
file_menu.add_command(label="Open", command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
menu_bar.add_cascade(label="File", menu=file_menu)

# Edit Menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Copy", command=copy_text, accelerator="Ctrl+C")
edit_menu.add_command(label="Paste", command=paste_text, accelerator="Ctrl+V")
edit_menu.add_command(label="Select All", command=select_all, accelerator="Ctrl+A")
edit_menu.add_command(label="Open", command=open_file, accelerator="Ctrl+O")
edit_menu.add_separator()
edit_menu.add_command(label="Font Size...", command=change_font_size)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# Help Menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menu_bar)

# --- Shortcut Bindings ---
root.bind("<Control-n>", new_file)
root.bind("<Control-o>", open_file)
root.bind("<Control-s>", save_file)
root.bind("<Control-c>", lambda e: copy_text())
root.bind("<Control-v>", lambda e: paste_text())
root.bind("<Control-a>", lambda e: select_all())

# Override window close button
root.protocol("WM_DELETE_WINDOW", exit_app)

# --- Handle double-clicked file argument ---
if len(sys.argv) > 1:
    file_path = os.path.abspath(sys.argv[1].strip('"'))
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="latin-1") as f:
            content = f.read()
    except Exception as e:
        messagebox.showerror("Error", f"Could not open file:\n{e}")
        content = ""
    text_area.insert(tk.END, content)
    current_file = file_path
    is_saved = True
    update_title()

update_title()
root.mainloop()
