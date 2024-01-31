from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn ={}
# Read csv data
# if file not found error found
try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# function to generate word
def generate_word():
    global current_card, card_timer
    window.after_cancel(card_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfigure(language_name, text="French", fill="black")
    canvas.itemconfigure(language_word, text=current_card["French"], fill="black")
    canvas.itemconfigure(canvas_img, image=card_front)
    card_timer = window.after(3000, func=flip_card)
# this function flip the card
def flip_card():
    canvas.itemconfigure(canvas_img, image=card_back)
    canvas.itemconfigure(language_name, text="English", fill="white")
    canvas.itemconfigure(language_word, text=current_card["English"], fill="white")

# if user know the word then remove the word from the dicionary and save the remaining word into words to learn csv ( a new file).
def remove_word():
    to_learn.remove(current_card)
    data = pd.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    generate_word()

# create window
window = Tk()
window.title("Flash card", )
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
card_timer = window.after(3000, func=flip_card)

# create canvas
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
# create front card image
card_front = PhotoImage(file="images/card_front.png")
# create back card image
card_back = PhotoImage(file="images/card_back.png")
canvas_img = canvas.create_image(400, 263, image=card_front)
language_name = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
language_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# create right button
right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, relief=FLAT, bg=BACKGROUND_COLOR, command=remove_word)
right_button.grid(row=1, column=1)

# create wrong button
wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, relief=FLAT, bg=BACKGROUND_COLOR, command=generate_word)
wrong_button.grid(row=1, column=0, )

generate_word()
window.mainloop()
