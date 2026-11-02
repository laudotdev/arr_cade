import tkinter as tk

#colors
BG = "#000000"
CARD_BORDER = "#2a2a2a"
TEXT = "#e8e8e8"
MUTED = "#b5b5b5"
SELECTED = "#2d5fb4"
GREEN = "#3ddc6a"
GREEN_BG = "#0f2a18"
RED = "#e5484d"

DEFAULT_ARRAY = [12, 25, 38, 41, 56]

#app state
data = list(DEFAULT_ARRAY)
selected = 4

root = tk.Tk()
root.title("Arr-Cade")
root.configure(bg=BG)
root.geometry("560x640")
root.minsize(560, 640)
root.resizable(True, True)


def toggle_fullscreen(event=None):
    #f11 switches fullscreen on and off
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))


def exit_fullscreen(event=None):
    #escape leaves fullscreen
    root.attributes("-fullscreen", False)


root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", exit_fullscreen)

#start maximized when the window system supports it
try:
    root.state("zoomed")
except tk.TclError:
    try:
        root.attributes("-zoomed", True)
    except tk.TclError:
        pass

card = tk.Frame(root, bg=BG, highlightbackground=CARD_BORDER, highlightthickness=1)
card.pack(fill="both", expand=True, padx=6, pady=6)

#header
header = tk.Frame(card, bg=BG)
header.pack(fill="x", padx=12, pady=(12, 0))
tk.Label(header, text="ARRAY PLAYGROUND", bg=BG, fg=TEXT,
         font=("Segoe UI", 10, "bold")).pack(side="left")
tk.Label(header, text="Interactive concept", bg=GREEN_BG, fg=GREEN,
         font=("Segoe UI", 7), padx=6).pack(side="right")

tk.Label(card, text="VISUAL ARRAY REPRESENTATION", bg=BG, fg=MUTED,
         font=("Segoe UI", 7)).pack(anchor="w", padx=12, pady=(6, 4))

#grid where the array cells are drawn
grid = tk.Frame(card, bg=BG)
grid.pack(fill="x", padx=12)
for c in range(3):
    grid.columnconfigure(c, weight=1, uniform="col")

info_label = tk.Label(card, text="", bg=BG, fg=MUTED, font=("Segoe UI", 7))
info_label.pack(anchor="w", padx=12, pady=(6, 0))

tk.Frame(card, bg=CARD_BORDER, height=1).pack(fill="x", padx=12, pady=10)

#operations section
tk.Label(card, text="Array Operations", bg=BG, fg=TEXT,
         font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=12)

tk.Label(card, text="Value", bg=BG, fg=TEXT,
         font=("Segoe UI", 8)).pack(anchor="w", padx=12, pady=(8, 2))
value_entry = tk.Entry(card, bg=BG, fg=TEXT, insertbackground=TEXT, relief="flat",
                       highlightbackground=CARD_BORDER, highlightcolor=CARD_BORDER,
                       highlightthickness=1, font=("Segoe UI", 10))
value_entry.pack(fill="x", padx=12, ipady=6)
value_entry.insert(0, "")

tk.Label(card, text="Index", bg=BG, fg=TEXT,
         font=("Segoe UI", 8)).pack(anchor="w", padx=12, pady=(8, 2))
index_entry = tk.Entry(card, bg=BG, fg=TEXT, insertbackground=TEXT, relief="flat",
                       highlightbackground=CARD_BORDER, highlightcolor=CARD_BORDER,
                       highlightthickness=1, font=("Segoe UI", 10))
index_entry.pack(fill="x", padx=12, ipady=6)
index_entry.insert(0, "5")

#buttons
buttons = tk.Frame(card, bg=BG)
buttons.pack(fill="x", padx=12, pady=(10, 0))
buttons.columnconfigure(0, weight=1, uniform="b")
buttons.columnconfigure(1, weight=1, uniform="b")

array_label = tk.Label(card, text="", bg=BG, fg=TEXT, font=("Segoe UI", 9))
status_label = tk.Label(card, text="", bg=BG, fg=MUTED, font=("Segoe UI", 7))


def draw():
    #redraw every cell from the list
    for w in grid.winfo_children():
        w.destroy()
    for i, v in enumerate(data):
        is_sel = (i == selected)
        bg = SELECTED if is_sel else BG
        cell = tk.Frame(grid, bg=bg, cursor="hand2")
        cell.grid(row=i // 3, column=i % 3, sticky="nsew", padx=4, pady=4, ipady=6)
        l1 = tk.Label(cell, text="Index " + str(i), bg=bg, fg=TEXT, font=("Segoe UI", 8, "bold"))
        l2 = tk.Label(cell, text=str(v), bg=bg, fg="white", font=("Segoe UI", 12, "bold"))
        l1.pack(pady=(6, 0))
        l2.pack(pady=(2, 6))
        for w in (cell, l1, l2):
            w.bind("<Button-1>", lambda e, idx=i: select(idx))
    size = len(data)
    sel_text = str(selected) if selected is not None else "none"
    info_label.config(text="Selected index: " + sel_text + " \u00b7 Array size: " + str(size))
    array_label.config(text="[" + ", ".join(str(x) for x in data) + "]")


def select(i):
    #click a cell to select it and fill the index box
    global selected
    selected = i
    index_entry.delete(0, "end")
    index_entry.insert(0, str(i))
    draw()


def say(msg, error=False):
    status_label.config(text=msg, fg=RED if error else MUTED)


def get_value():
    #read the value box as a number
    try:
        return int(value_entry.get().strip())
    except ValueError:
        say("Value must be a whole number.", True)
        return None


def get_index():
    #read the index box as a number
    try:
        return int(index_entry.get().strip())
    except ValueError:
        say("Index must be a whole number.", True)
        return None


def append():
    global selected
    v = get_value()
    if v is None:
        return
    data.append(v)
    selected = len(data) - 1
    say("Appended " + str(v) + " at index " + str(selected) + ".")
    draw()


def insert():
    global selected
    v = get_value()
    i = get_index()
    if v is None or i is None:
        return
    if i < 0 or i > len(data):
        say("Index must be between 0 and " + str(len(data)) + " for insert.", True)
        return
    data.insert(i, v)
    selected = i
    say("Inserted " + str(v) + " at index " + str(i) + ".")
    draw()


def update():
    global selected
    v = get_value()
    i = get_index()
    if v is None or i is None:
        return
    if i < 0 or i >= len(data):
        say("Index must be between 0 and " + str(len(data) - 1) + " for update.", True)
        return
    data[i] = v
    selected = i
    say("Updated index " + str(i) + " to " + str(v) + ".")
    draw()


def delete():
    global selected
    i = get_index()
    if i is None:
        return
    if i < 0 or i >= len(data):
        say("Index must be between 0 and " + str(len(data) - 1) + " for delete.", True)
        return
    removed = data.pop(i)
    if len(data) == 0:
        selected = None
    else:
        selected = min(i, len(data) - 1)
    say("Deleted " + str(removed) + " from index " + str(i) + ".")
    draw()


def reset():
    global data, selected
    data = list(DEFAULT_ARRAY)
    selected = 4
    value_entry.delete(0, "end")
    value_entry.insert(0, "99")
    index_entry.delete(0, "end")
    index_entry.insert(0, "5")
    say("Array reset.")
    draw()


def make_button(text, command, row, col, light=False, danger=False):
    #one style for all four main buttons
    if light:
        bg, fg = "#ebebeb", "#111111"
    else:
        bg, fg = BG, RED if danger else TEXT
    border = "#5a2528" if danger else CARD_BORDER
    b = tk.Button(buttons, text=text, command=command, bg=bg, fg=fg, relief="flat",
                  activebackground=bg, activeforeground=fg, cursor="hand2",
                  highlightbackground=border, highlightthickness=1, font=("Segoe UI", 8))
    b.grid(row=row, column=col, sticky="ew", padx=3, pady=3, ipady=4)


make_button("Append", append, 0, 0, light=True)
make_button("Insert", insert, 0, 1)
make_button("Update", update, 1, 0)
make_button("Delete", delete, 1, 1, danger=True)

#current array row
row = tk.Frame(card, bg=BG)
row.pack(fill="x", padx=12, pady=(10, 0))
tk.Label(row, text="Current array", bg=BG, fg=MUTED, font=("Segoe UI", 7)).pack(side="left")
reset_btn = tk.Label(row, text="Reset", bg=BG, fg=TEXT, font=("Segoe UI", 8), cursor="hand2")
reset_btn.pack(side="right")
reset_btn.bind("<Button-1>", lambda e: reset())

array_label.pack(anchor="w", padx=12, pady=(10, 6))
status_label.pack(anchor="w", padx=12, pady=(0, 10))
say("Working interactive demonstration. Insert, update, append and delete are demonstrated visually.")

draw()
root.mainloop()