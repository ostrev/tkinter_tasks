import string
from random import choice
from tkinter import *
from tkinter import ttk, messagebox


class HangmanCalc:
    def __init__(self, word):
        self.word = word
        self.letter = ''
        self.count = 1
        self.result = ['_' for _ in range(len(self.word))]

    def display_word(self):
        for i in range(len(self.word)):
            if self.result[i] == '_':
                if self.word[i] == self.word[0]:
                    self.result[i] = self.word[0]
                elif self.word[i] == self.word[-1]:
                    self.result[i] = self.word[-1]
                elif self.word[i] == self.letter:
                    self.result[i] = self.letter
                else:
                    self.result[i] = '_'
        return ''.join(self.result)

    def calc_count(self):
        if self.letter not in self.word:
            self.count += 1


class HangmanApp:
    def __init__(self, root, random_word):
        self.root = root
        self.random_word = random_word
        self.root.title("Hangman Game")
        self.root.bind("<Key>", self.on_key_press)

        self.buttons = {}
        self.display_buttons()

        self.game = HangmanCalc(random_word)

        self.change_image()

        self.game.display_word()

        self.label_attempts = ttk.Label(root, text=f"Remaining Attempts: {8 - self.game.count}")
        self.label_attempts.grid(row=0, column=1, columnspan=13)

        self.label_word = ttk.Label(root, text=self.game.display_word(), font=("Helvetica", 24))
        self.label_word.grid(row=1, column=1, columnspan=13)

    def change_image(self):
        value = self.game.count
        image_name = f'{value}.png'
        image_width = 450
        image_height = 600
        image = PhotoImage(file=image_name, width=image_width, height=image_height)

        image_label = Label()
        image_label.grid(row=0, column=0, rowspan=2)

        image_label.config(image=image)
        image_label.image = image

    def on_key_press(self, event):
        letter = event.char.lower()
        if letter.isalpha() and letter in self.buttons:
            self.on_button_click(letter)

    def on_button_click(self, letter):
        self.buttons[letter].config(state=DISABLED)

        self.game.letter = letter
        self.game.display_word()
        self.game.calc_count()
        self.change_image()
        self.update_display()

        if self.game.count == 8:
            messagebox.showinfo("Game Over", "You lost! The word was: " + self.game.word)
            self.root.quit()
        elif self.game.display_word() == self.game.word:
            messagebox.showinfo("Congratulations", "You won!")
            self.root.quit()

    def display_buttons(self):
        alphabet = string.ascii_lowercase
        for i, letter in enumerate(alphabet):
            row = i // 13
            column = i % 13
            button = ttk.Button(root, text=letter, command=lambda l=letter: self.on_button_click(l), width=2)
            button.grid(row=2 + row, column=1 + column)
            self.buttons[letter] = button

        self.buttons[self.random_word[0]].config(state=DISABLED)
        self.buttons[self.random_word[-1]].config(state=DISABLED)

    def update_display(self):
        self.label_word.config(text=self.game.display_word())
        self.label_attempts.config(text=f"Remaining Attempts: {8 - self.game.count}")


if __name__ == "__main__":
    word_list = [
        'apple', 'banana', 'orange', 'cherry', 'lemon', 'peach', 'grape',
        'tomato', 'carrot', 'potato', 'broccoli', 'lettuce', 'pepper', 'onion', 'garlic',
        'melon', 'pineapple', 'berry', 'apricot', 'mango', 'bean', 'cabbage',
        'pumpkin', 'radish', 'zucchini', 'celery', 'eggplant', 'cucumber', 'asparagus',
        'grapefruit', 'avocado', 'nectarine', 'watermelon', 'coconut', 'blueberry',
        'strawberry', 'raspberry', 'blackberry', 'pomegranate', 'cranberry', 'walnut', 'almond',
        'cashew', 'chestnut', 'hazelnut', 'macadamia', 'pecan', 'pistachio', 'peanut', 'nutmeg',
        'cinnamon', 'vanilla', 'chocolate', 'honey', 'maple', 'sugar', 'flour', 'butter',
        'vinegar', 'pepper', 'garlic', 'onion', 'basil', 'oregano', 'thyme', 'parsley',
        'rosemary', 'coriander', 'cumin', 'turmeric', 'paprika', 'saffron', 'cardamom', 'chili',
        'curry', 'ginger', 'cloves', 'nutmeg', 'tarragon', 'cayenne', 'mustard',
        'wasabi', 'tamari', 'teriyaki', 'hoisin', 'sriracha', 'ketchup', 'mayonnaise'
    ]
    random_word = choice(word_list)
    print(random_word)
    root = Tk()
    root.geometry('1200x800')

    app = HangmanApp(root, random_word)

    for child in root.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()
