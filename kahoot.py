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

NORMAL_FONT = ("consolas", 20)


###############################################################################
#    Functions:
###############################################################################

def start(question_number,score):

    num_choices = len(choices[question_number])
    button_dimension = int(GAME_DIMENSION/(num_choices+1))

    question_label = tk.Label(text=questions[question_number],
                              wraplength=GAME_DIMENSION,
                              font=NORMAL_FONT,
                              bg="white",
                              fg="black")

    question_label.place(width=GAME_DIMENSION,
                         height=button_dimension,
                         x=0,
                         y=0)

    for i, choice in enumerate(choices[question_number]):

        choice_button = tk.Button(window,
                                  text=choice,
                                  wraplength=GAME_DIMENSION,
                                  font=NORMAL_FONT,
                                  bg="white",
                                  highlightbackground="white",
                                  fg="black",
                                  command=lambda choice=choice:
                                  check_answer(choice,question_number,score)
                                  )

        choice_button.place(width=GAME_DIMENSION,
                            height=button_dimension,
                            x=0,
                            y=(i+1)*button_dimension)

def check_answer(choice,question_number,score):


    if choice == answers_list[question_number]:
        print(1)
        score += 1
        score_label = tk.Label(text="Correct",
                                wraplength=GAME_DIMENSION,
                                font=NORMAL_FONT,
                                bg="green",
                                fg="black")
        
        score_label.place(width=GAME_DIMENSION,
                            height=GAME_DIMENSION,
                            x=0,
                            y=0)
    else:
        print(0)
        score_label = tk.Label(text="Incorrect",
                                wraplength=GAME_DIMENSION,
                                font=NORMAL_FONT,
                                bg="red",
                                fg="black")
        
        score_label.place(width=GAME_DIMENSION,
                            height=GAME_DIMENSION,
                            x=0,
                            y=0)

    window.after(500, lambda: next_question(question_number, score))


def next_question(question_number, score):

    # Remove past buttons
    for child in canvas.winfo_children():
        child.destroy()

    question_number += 1

    if question_number < total_questions:
        start(question_number,score)
    else:
        end_label = tk.Label(text='Finished, score: ' + str(score),
                             wraplength=GAME_DIMENSION,
                             font=NORMAL_FONT,
                             bg="white",
                             fg="black")

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

print(answers_list)

#randomized questions version below ----
#populate the questions with the questions from the scraped data, and have it so the questions are randomized if we are pulling more than 25 questions 
# shuffled_list = list(questions_and_choices.items())
# random.shuffle(shuffled_list)
# shuffled_data = dict(shuffled_list)
# questions = list(shuffled_data.keys())
# choices = list(shuffled_data.values())
#----

total_questions = len(questions)
total_questions = 10

window = tk.Tk()
window.title("Kahoot Game")
window.resizable(False, False)

# Create the canvas for the game.
canvas = tk.Canvas(window,
                   bg="white",
                   height=GAME_DIMENSION,
                   width=GAME_DIMENSION)

# Pack the canvas.
canvas.pack()

# Update the game window.
window.update()

start(0,0)

# Run the main loop of the program.
tk.mainloop()