import tkinter as tk
from tkinter import messagebox
import random
from categories import CATEGORIES

BG = "#F3F6FC"
NAVY = "#253B80"
BLUE = "#3975D7"
GREEN = "#239B56"
RED = "#D9534F"
TEXT = "#24324A"


class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman World")
        self.root.geometry("980x760")
        self.root.minsize(850, 680)
        self.root.configure(bg=BG)

        self.category = None
        self.score = 0
        self.word = ""
        self.guessed = set()
        self.wrong = 0
        self.game_over = False
        self.hint_used = False

        self.player_name = ""
        self.show_name_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def header(self, subtitle):
        top = tk.Frame(self.root, bg=NAVY, height=95)
        top.pack(fill="x")
        tk.Label(top, text="HANGMAN WORLD", font=("Arial", 25, "bold"),
                 bg=NAVY, fg="white").pack(pady=(15, 3))
        tk.Label(top, text=subtitle, font=("Arial", 11),
                 bg=NAVY, fg="#DCE6FF").pack()

    def show_name_screen(self):
        self.clear_screen()

        self.header("Welcome to the Hangman Challenge!")

        container = tk.Frame(self.root, bg=BG)
        container.pack(expand=True)

        tk.Label(
            container,
            text="🎮 HANGMAN WORLD",
            font=("Arial", 25, "bold"),
            bg=BG,
            fg=NAVY
        ).pack(pady=20)

        tk.Label(
            container,
            text="What should we call you?",
            font=("Arial", 16, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(pady=10)

        self.name_entry = tk.Entry(
            container,
            font=("Arial", 16),
            width=25,
            justify="center"
        )
        self.name_entry.pack(pady=15)
        self.name_entry.focus()

        tk.Button(
            container,
            text="START GAME →",
            font=("Arial", 13, "bold"),
            bg=GREEN,
            fg="white",
            width=20,
            height=2,
            command=self.submit_player_name
        ).pack(pady=15)

    def submit_player_name(self):

        name = self.name_entry.get().strip()

        if not name:
            messagebox.showwarning(
                "Name Required",
                "Please enter your name before continuing!"
            )
            return

        self.player_name = name

        self.show_category_screen()

    def show_category_screen(self):
        self.clear_screen()
        self.header("Choose a category and start guessing!")
        tk.Label(self.root, text="SELECT YOUR CATEGORY",
                 font=("Arial", 19, "bold"), bg=BG, fg=NAVY).pack(pady=(18, 5))
        tk.Label(self.root, text=f"{len(CATEGORIES)} categories  •  20 words in each category",
                 font=("Arial", 11), bg=BG, fg="#63718A").pack(pady=(0, 12))

        # Scrollable category grid
        outer = tk.Frame(self.root, bg=BG)
        outer.pack(fill="both", expand=True, padx=35, pady=5)
        canvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        grid_frame = tk.Frame(canvas, bg=BG)
        grid_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=grid_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.category_var = tk.StringVar(value="")
        self.category_buttons = {}
        for index, category in enumerate(CATEGORIES):
            row, col = divmod(index, 3)
            btn = tk.Radiobutton(
                grid_frame, text=category, variable=self.category_var,
                value=category, indicatoron=False, width=25, height=2,
                font=("Arial", 11, "bold"), bg="white", fg=TEXT,
                selectcolor="#DCEAFE", activebackground="#E8F0FF",
                relief="ridge", bd=1, command=self.update_category_selection
            )
            btn.grid(row=row, column=col, padx=9, pady=7, sticky="ew")
            self.category_buttons[category] = btn
        for col in range(3):
            grid_frame.grid_columnconfigure(col, weight=1)

        self.selection_label = tk.Label(self.root, text="No category selected",
                                        font=("Arial", 11), bg=BG, fg="#63718A")
        self.selection_label.pack(pady=7)
        tk.Button(self.root, text="NEXT  →", font=("Arial", 13, "bold"),
                  bg=GREEN, fg="white", activebackground="#1E8449",
                  width=18, height=2, bd=0, command=self.start_category_game).pack(pady=(0, 18))

    def update_category_selection(self):
        chosen = self.category_var.get()
        self.selection_label.config(text=f"Selected category: {chosen}",
                                    fg=NAVY)

    def start_category_game(self):
        chosen = self.category_var.get()
        if not chosen:
            messagebox.showwarning("Choose a category", "Please select a category first.")
            return
        self.category = chosen
        self.start_game_screen()

    def start_game_screen(self):
        self.clear_screen()
        self.header(f"Category: {self.category}")
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=25, pady=15)

        left = tk.Frame(body, bg="white", bd=1, relief="solid")
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))
        tk.Label(left, text="HANGMAN", font=("Arial", 15, "bold"),
                 bg="white", fg=NAVY).pack(pady=(15, 5))
        self.canvas = tk.Canvas(left, width=390, height=340,
                                bg="white", highlightthickness=0)
        self.canvas.pack(padx=10, pady=5)

        right = tk.Frame(body, bg=BG)
        right.pack(side="right", fill="both", expand=True, padx=(12, 0))
        tk.Label(right, text="GUESS THE WORD", font=("Arial", 16, "bold"),
                 bg=BG, fg=NAVY).pack(pady=(10, 18))
        self.word_label = tk.Label(right, text="", font=("Arial", 23, "bold"),
                                   bg=BG, fg=NAVY, wraplength=430)
        self.word_label.pack(pady=15)
        self.attempt_label = tk.Label(right, text="", font=("Arial", 12, "bold"),
                                      bg=BG, fg=RED)
        self.attempt_label.pack(pady=7)
        self.score_label = tk.Label(right, text="", font=("Arial", 12, "bold"),
                                    bg=BG, fg=NAVY)
        self.score_label.pack(pady=7)
        self.message_label = tk.Label(right, text="Choose a letter to begin!",
                                      font=("Arial", 11), bg=BG, fg=TEXT,
                                      wraplength=380)
        self.message_label.pack(pady=12)
        self.hint_button = tk.Button(right, text="💡 Show Hint",
                                     font=("Arial", 11, "bold"), bg="#F0AD4E",
                                     fg="white", width=17, bd=0,
                                     command=self.show_hint)
        self.hint_button.pack(pady=8)

        alphabet_area = tk.Frame(self.root, bg=BG)
        alphabet_area.pack(pady=4)
        tk.Label(alphabet_area, text="CHOOSE A LETTER",
                 font=("Arial", 12, "bold"), bg=BG, fg=NAVY).pack(pady=5)
        self.letters_frame = tk.Frame(alphabet_area, bg=BG)
        self.letters_frame.pack()
        self.letter_buttons = {}
        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            button = tk.Button(self.letters_frame, text=letter,
                               font=("Arial", 10, "bold"), width=4,
                               bg=NAVY, fg="white", activebackground=BLUE,
                               command=lambda x=letter: self.guess_letter(x))
            button.grid(row=i // 13, column=i % 13, padx=3, pady=4)
            self.letter_buttons[letter] = button

        bottom = tk.Frame(self.root, bg=BG)
        bottom.pack(pady=(8, 15))
        tk.Button(bottom, text="↻ Play Again", font=("Arial", 11, "bold"),
                  bg=GREEN, fg="white", width=15, bd=0,
                  command=self.new_word).grid(row=0, column=0, padx=7)
        tk.Button(bottom, text="← Categories", font=("Arial", 11, "bold"),
                  bg=BLUE, fg="white", width=15, bd=0,
                  command=self.show_category_screen).grid(row=0, column=1, padx=7)
        tk.Button(bottom, text="Exit", font=("Arial", 11, "bold"),
                  bg=RED, fg="white", width=12, bd=0,
                  command=self.root.destroy).grid(row=0, column=2, padx=7)

        self.new_word()

    def new_word(self):
        self.word = random.choice(CATEGORIES[self.category]).upper()
        self.guessed = set()
        self.wrong = 0
        self.game_over = False
        self.hint_used = False
        for letter, button in self.letter_buttons.items():
            button.config(state="normal", bg=NAVY, fg="white")
        self.hint_button.config(state="normal")
        self.message_label.config(text="Choose a letter to begin!", fg=TEXT)
        self.update_word()
        self.update_status()
        self.draw_hangman()

    def update_word(self):
        # Spaces and hyphens are shown automatically; only letters are hidden.
        shown = [ch if ch == " " or ch == "-" or ch in self.guessed else "_" for ch in self.word]
        self.word_label.config(text="  ".join(shown))

    def update_status(self):
        self.attempt_label.config(text=f"Remaining attempts: {6 - self.wrong}")
        self.score_label.config(text=f"Score: {self.score}")

    def guess_letter(self, letter):
        if self.game_over or letter in self.guessed:
            return
        self.guessed.add(letter)
        button = self.letter_buttons[letter]
        button.config(state="disabled")
        if letter in self.word:
            button.config(bg=GREEN)
            self.message_label.config(text="Correct! Well done.", fg=GREEN)
            self.update_word()
            if all(ch == " " or ch == "-" or ch in self.guessed for ch in self.word):
                self.win_game()
        else:
            button.config(bg=RED)
            self.wrong += 1
            self.message_label.config(text="Not in the word. Try again!", fg=RED)
            self.draw_hangman()
            self.update_status()
            if self.wrong >= 6:
                self.lose_game()

    def show_hint(self):
        if self.game_over or self.hint_used:
            return
        self.hint_used = True
        self.hint_button.config(state="disabled")
        self.message_label.config(text="Hint: The answer belongs to " + self.category + ".", fg="#B7791F")

    def draw_hangman(self):
        self.canvas.delete("all")
        # Gallows
        self.canvas.create_line(55, 315, 300, 315, width=5, fill="#354052")
        self.canvas.create_line(105, 315, 105, 35, width=5, fill="#354052")
        self.canvas.create_line(105, 35, 250, 35, width=5, fill="#354052")
        self.canvas.create_line(250, 35, 250, 70, width=4, fill="#354052")
        if self.wrong >= 1:
            self.canvas.create_oval(220, 70, 280, 130, width=4, outline=RED)
        if self.wrong >= 2:
            self.canvas.create_line(250, 130, 250, 215, width=4, fill=RED)
        if self.wrong >= 3:
            self.canvas.create_line(250, 150, 205, 185, width=4, fill=RED)
        if self.wrong >= 4:
            self.canvas.create_line(250, 150, 295, 185, width=4, fill=RED)
        if self.wrong >= 5:
            self.canvas.create_line(250, 215, 210, 270, width=4, fill=RED)
        if self.wrong >= 6:
            self.canvas.create_line(250, 215, 290, 270, width=4, fill=RED)

    def win_game(self):

        self.game_over = True
        self.score += 1
        self.update_status()

        self.message_label.config(
            text=f"🎉 AMAZING, {self.player_name.upper()}! "
                 f"YOU DID IT! WORD: {self.word}",
            fg=GREEN
        )

        self.disable_letters()

        self.root.after(2500, self.new_word)
        self.root.after(1400, self.new_word)
    def lose_game(self):
        self.game_over = True
        self.update_word()
        self.message_label.config(text=f"Game over! The word was {self.word}.", fg=RED)
        self.disable_letters()
        messagebox.showinfo("Game over", f"Better luck next time!\nThe word was {self.word}.")

    def disable_letters(self):
        for button in self.letter_buttons.values():
            button.config(state="disabled")
        self.hint_button.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanGame(root)
    root.mainloop()
