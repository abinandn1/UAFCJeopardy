###############################################################################
#    INCLUDES:
###############################################################################

import time
import tkinter as tk # Used to create game interface.
from tkinter import messagebox
from bs4 import BeautifulSoup
from webscraping import scrape_questions_and_answers
import random # Allows randomization of questions pulled for a Kahoot game 

###############################################################################
#    CONSTANTS:
###############################################################################

GAME_DIMENSION = 700
BUTTON_DIMENSION = 140

BACKGROUND_COLOR = "white"
TEXT_COLOR = "black"

DEFAULT_COLOR = 'white'
CORRECT_COLOR = 'green'
INCORRECT_COLOR = 'red'

NORMAL_FONT_SIZE = 20
NORMAL_FONT = ("consolas", NORMAL_FONT_SIZE)


###############################################################################
#    Functions:
###############################################################################

def start(question_number,score):

    # Remove past buttons
    for child in window.winfo_children():
        child.destroy()

    question_label = tk.Label(text=questions[question_number],
                              wraplength=GAME_DIMENSION,
                              font=NORMAL_FONT,
                              bg=BACKGROUND_COLOR,
                              fg=TEXT_COLOR)

    question_label.place(width=GAME_DIMENSION,
                         height=BUTTON_DIMENSION,
                         x=0,
                         y=0)

    button_number = 0
    for choice in choices[question_number]:

        choice_button = tk.Button(window,
                                  text=choice,
                                  wraplength=GAME_DIMENSION,
                                  font=NORMAL_FONT,
                                  bg=DEFAULT_COLOR,
                                  highlightbackground=DEFAULT_COLOR,
                                  fg=TEXT_COLOR,
                                  command=lambda selection=choice:
                                  answer_callback(question_number,choice_button,score)
                                  )

        choice_button.place(width=GAME_DIMENSION,
                            height=BUTTON_DIMENSION,
                            x=0,
                            y=(button_number+1)*BUTTON_DIMENSION)

        button_number += 1

    def answer_callback(question_number,selection,score):

        print(choices[question_number])
        print(selection)
        print(answers_list[question_number])

        if selection == answers_list[question_number]:
            score += 1

        question_number += 1

        # if question_number < total_questions:
        if question_number < 2:
            start(question_number,score)
        else:

            # Remove past buttons
            for child in window.winfo_children():
                child.destroy()

            end_label = tk.Label(text='Finished, score: ' + str(score),
                                 wraplength=GAME_DIMENSION,
                                 font=NORMAL_FONT,
                                 bg=BACKGROUND_COLOR,
                                 fg=TEXT_COLOR)

            end_label.place(width=GAME_DIMENSION,
                            height=GAME_DIMENSION,
                            x=0,
                            y=0)

###############################################################################
#    MAIN:
###############################################################################

webscraping_data = scrape_questions_and_answers()

questions = list()
choices = list()
answers_list = list()
for question, answers in webscraping_data.items():
    questions.append(question)
    choices.append(answers[0])
    if answers[1]:
        answers_list.append(answers[1][0])

#randomized questions version below ----
#populate the questions with the questions from the scraped data, and have it so the questions are randomized if we are pulling more than 25 questions 
# shuffled_list = list(questions_and_choices.items())
# random.shuffle(shuffled_list)
# shuffled_data = dict(shuffled_list)
# questions = list(shuffled_data.keys())
# choices = list(shuffled_data.values())
#----

total_questions = len(questions)

window = tk.Tk()
window.title("Kahoot Game")
window.resizable(False, False)

# Create the canvas for the game.
canvas = tk.Canvas(window,
                   bg=BACKGROUND_COLOR,
                   height=GAME_DIMENSION,
                   width=GAME_DIMENSION)

# Pack the canvas.
canvas.pack()

# Update the game window.
window.update()

start(0,0)

# Run the main loop of the program.
tk.mainloop()