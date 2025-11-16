from tkinter import *
from tkinter import messagebox
import random

root = Tk()
root.title("Alexa - Tell me a Joke")
root.geometry("450x400")
root.iconbitmap("Alexa.ico")

gradient = Canvas(root, width=450, height=400, highlightthickness=0)
gradient.pack(fill="both", expand=True)

for i in range(400):
    color = f"#{int(223 - i/4):02x}{int(231 - i/6):02x}{int(245 - i/12):02x}"
    gradient.create_line(0, i, 450, i, fill=color)

card = Frame(root, bg="white")
card.place(relx=0.5, rely=0.5, anchor="center", width = 360, height= 300)

def load_jokes():
    jokes_list = []
    try:
        with open ("randomJokes.txt", "r", encoding="utf-8") as f:
            for line in f:
                if "?" in line:
                    setup, punchline = line.strip().split("?", 1)
                    jokes_list.append((setup + "?", punchline))
    
    except FileNotFoundError:
        messagebox.showerror("Error", "Could not Find 'randomJokes.txt'!")
    return jokes_list

def clear_frame():
    for widget in card.winfo_children():
        widget.destroy()

def lighten(color_hex):
    color_hex = color_hex.lstrip('#')
    r = min (255, int(color_hex[0:2], 16) +25)
    g = min (255, int(color_hex[2:4], 16) +25)
    b = min (255, int(color_hex[4:6], 16) +25)
    return f"#{r:02x}{g:02x}{b:02x}"

def button(parent, text, command, bg = "#1a73e8"):
    btn = Button(
        parent,
        text=text,
        command=command,
        font=("Comic Sans MS", 12, "bold"),
        fg="white",
        bg=bg,
        activebackground=bg,
        relief="flat",
        padx=18,
        pady=10,
        bd=0,
    )

    def on_enter(e):
        btn.config(bg=lighten(bg))
    def on_leave(e):
        btn.config(bg=bg)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

    return btn

def alexa_button(parent, command):
    canvas = Canvas(parent, width=140, height=140, bg="white", highlightthickness=0)
    canvas.pack(pady=15)

    canvas.create_oval(10, 10, 130, 130, fill="#b3d4ff", outline="#b3d4ff")
    center_circle = canvas.create_oval(25, 25, 115, 115, fill="#1a73e8", outline="#1a73e8")
    canvas.create_text(70, 70, text="Alexa", fill="white", font=("Comic Sans MS", 16, "bold"))

    canvas.bind("<Button-1>", lambda e:command())

    def hover_in(e):
        canvas.itemconfig(center_circle, fill= "#2e82ff")

    def hover_out(e):
        canvas.itemconfig(center_circle, fill="#1a73e8")

    canvas.bind("<Enter>", hover_in)
    canvas.bind("<Leave>", hover_out)

    return canvas
def show_joke():
    global current_joke
    clear_frame()
    current_joke = random.choice(jokes)

    Label(
        card,
        text=current_joke[0],
        wraplength=330,
        font=("Comic Sans MS", 14),
        bg="white",
        fg="#333"
    ).pack(pady=25)

    button(card, "Show Punchline", show_punchline).pack(pady=8)

def show_punchline():
        clear_frame()

        Label(
            card,
            text= current_joke[1],
            wraplength=330,
            font=("Comic Sans MS",16,"bold"),
            fg= "#1a73e8",
            bg="white"
        ).pack(pady=25)

        button(card, "Another Joke", show_joke).pack(pady=8)
        button(card, "Quit", root.destroy, bg="#e74c3c").pack(pady=5)

def main_prompt():
        clear_frame()

        Label(
            card,
            text="Tap Alexa to hear a joke",
            font=("Comic Sans MS", 14, "bold"),
            bg="white",
            fg="#333"
        ).pack(pady=10)

        alexa_button(card,show_joke)
        button(card, "Quit", root.destroy, bg="#e74c3c").pack(pady=10)

jokes = load_jokes()
main_prompt()
root.mainloop()