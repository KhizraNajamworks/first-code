import tkinter as tk
from tkinter import messagebox

# --- LAYER 1: THE CANVAS (Window Setup) ---
root = tk.Tk()
root.title("📱 KHIZRA'S CALC")       # Custom brand title updated!
root.geometry("380x570")
root.configure(bg="#B30046")       # Vibrant Deep Cherry Base Color
root.resizable(False, False)

current_expression = ""

# --- LAYER 2: THE LOGIC BRAIN (Math Functions) ---
def press_button(item):
    global current_expression
    current_expression += str(item)
    display_var.set(current_expression)

def clear_display():
    global current_expression
    current_expression = ""
    display_var.set("")

def calculate_result():
    global current_expression
    try:
        result = str(eval(current_expression))
        display_var.set(result)
        current_expression = result 
    except ZeroDivisionError:
        messagebox.showerror("Math Error", "❌ Bruh... you cannot divide by zero.")
        clear_display()
    except Exception:
        messagebox.showerror("Error", "🤨 Sus calculation input. Let's reset.")
        clear_display()

# --- THE APP DISPLAY SCREEN ---
display_var = tk.StringVar()
display_screen = tk.Entry(
    root, 
    textvariable=display_var, 
    font=("Helvetica Neue", 32, "bold"), 
    bd=0, 
    width=14, 
    justify="right",
    bg="#FFF0F5",      # Lavender Blush Ultra-Light Pink Screen Surface
    fg="#B30046",      # Rich text color to match the outer body
)
display_screen.pack(pady=30, ipady=18, padx=24, fill="both")

# --- LAYER 3: UI CONFIGURATION (Your Custom Cherry Palette) ---
COLOR_BG = "#B30046"         # Vibrant Deep Cherry Pink
COLOR_NUM_KEYS = "#F3C6D5"   # Light Powder Pink from your image selection
COLOR_ACTIONS = "#E491AC"    # Mid-tone Rose Pink for (+, -, *, /) symbols
COLOR_SPECIAL = "#910038"    # Extra deep burgundy wine for contrast (= and C keys)
TEXT_DARK = "#231B24"        # High-readability charcoal text color for number keys

# Function to build stylized buttons consistently
def create_btn(text, row, col, bg_color=COLOR_NUM_KEYS, fg_color=TEXT_DARK, cmd=None):
    btn = tk.Button(
        button_grid_frame, 
        text=text, 
        font=("Helvetica Neue", 16, "bold"), 
        bg=bg_color, 
        fg=fg_color, 
        activebackground="#D47392",
        activeforeground="white",
        bd=0, 
        relief="flat",
        command=cmd
    )
    btn.grid(row=row, column=col, padx=7, pady=7, sticky="nsew")
    return btn

# Grid Framework Scaffolding
button_grid_frame = tk.Frame(root, bg=COLOR_BG)
button_grid_frame.pack(fill="both", expand=True, padx=20, pady=10)

# Sets up 5 rows and 4 columns that expand evenly
for i in range(5):
    button_grid_frame.rowconfigure(i, weight=1)
for j in range(4):
    button_grid_frame.columnconfigure(j, weight=1)

# --- GRID BUTTON LAYOUT DESIGN ---

# Row 0: Actions & Clear
create_btn("C", 0, 0, bg_color=COLOR_SPECIAL, fg_color="white", cmd=clear_display)
create_btn("(", 0, 1, bg_color=COLOR_ACTIONS, cmd=lambda: press_button("("))
create_btn(")", 0, 2, bg_color=COLOR_ACTIONS, cmd=lambda: press_button(")"))
create_btn("÷", 0, 3, bg_color=COLOR_ACTIONS, cmd=lambda: press_button("/"))

# Row 1: Numbers & Multiply
create_btn("7", 1, 0, cmd=lambda: press_button(7))
create_btn("8", 1, 1, cmd=lambda: press_button(8))
create_btn("9", 1, 2, cmd=lambda: press_button(9))
create_btn("×", 1, 3, bg_color=COLOR_ACTIONS, cmd=lambda: press_button("*"))

# Row 2: Numbers & Subtract
create_btn("4", 2, 0, cmd=lambda: press_button(4))
create_btn("5", 2, 1, cmd=lambda: press_button(5))
create_btn("6", 2, 2, cmd=lambda: press_button(6))
create_btn("−", 2, 3, bg_color=COLOR_ACTIONS, cmd=lambda: press_button("-"))

# Row 3: Numbers & Add
create_btn("1", 3, 0, cmd=lambda: press_button(1))
create_btn("2", 3, 1, cmd=lambda: press_button(2))
create_btn("3", 3, 2, cmd=lambda: press_button(3))
create_btn("+", 3, 3, bg_color=COLOR_ACTIONS, cmd=lambda: press_button("+"))

# Row 4: Zero, Decimal, Equals
create_btn("0", 4, 0, cmd=lambda: press_button(0))
create_btn(".", 4, 1, cmd=lambda: press_button("."))

# The Fixed Equals Button Configuration
equals_btn = create_btn("=", 4, 2, bg_color=COLOR_SPECIAL, fg_color="white", cmd=calculate_result)
equals_btn.grid(row=4, column=2, columnspan=2, padx=7, pady=7, sticky="nsew")

# --- RUN ENGINE LOOP ---
root.mainloop()
