import time
import tkinter as tk # Used to create game interface.
from tkinter import messagebox
from bs4 import BeautifulSoup
from webscraping import scrape_questions_and_answers
import random #to allow for randomization of questions pulled for a Jeopardy game 
###############################################################################
#    CONSTANTS:
###############################################################################

#bring in webscraping data
#oct 31:
webscraping_data = scrape_questions_and_answers()

GAME_DIMENSION = 700 # need to adjust this so that all text and stuff is displayed properly 
BUTTONS_PER_LINE = 5
BUTTON_DIMENSION = int(GAME_DIMENSION/BUTTONS_PER_LINE)
TITLE_SIZE = 50

BACKGROUND_COLOR = "white"
TEXT_COLOR = "black"

DEFAULT_COLOR = 'white'
CORRECT_COLOR = 'green'
INCORRECT_COLOR = 'red'

NORMAL_FONT_SIZE = 20
NORMAL_FONT = ("consolas", NORMAL_FONT_SIZE)

# Define the names of each section of the game.
LABEL_NAMES = ['Section 1',
               'Section 2',
               'Section 3',
               'Section 4',
               'Section 5']

# Define the names of each button within a section.
BUTTON_NAMES = ['$100',
                '$200',
                '$300',
                '$400',
                '$500']

# Define questions to be presented when each button is clicked.

QUESTIONS = [['Question 1',
             'Question 2',
             'Question 3',
             'Question 4',
             'Question 5'],
            ['Question 6',
             'Question 7',
             'Question 8',
             'Question 9',
             'Question 10'],
            ['Question 11',
             'Question 12',
             'Question 13',
             'Question 14',
             'Question 15'],
            ['Question 16',
             'Question 17',
             'Question 18',
             'Question 19',
             'Question 20'],
            ['Question 21',
             'Question 22',
             'Question 23',
             'Question 24',
             'Question 25']]

# answer choices for the matrix + placeholder choices, real choices get pulled in below 
ANSWER_CHOICES = [[["choice1","choice2","choice3","choice4"],
             ["choice1","choice2","choice3","choice4"],
             ["choice1","choice2","choice3","choice4"],
             ["choice1","choice2","choice3","choice4"],
             ["choice1","choice2","choice3","choice4"]],
            [["choice1","choice2","choice3","choice4"],
             ["choice1","choice2","choice3","choice4"],
             ["choice1","choice2","choice3","choice4"],
             ["choice1","choice2","choice3","choice4"],
             ["choice1","choice2","choice3","choice4"]],
            [["choice1","choice2","choice3","choice4"],
             ["choice1","choice2","choice3","choice4"],
             ["choice1","choice2","choice3","choice4"],
             ["choice1","choice2","choice3","choice4"],
             ["choice1","choice2","choice3","choice4"]],
            [["choice1","choice2","choice3","choice4"],
             ["choice1","choice2","choice3","choice4"],
             ["choice1","choice2","choice3","choice4"],
             ["choice1","choice2","choice3","choice4"],
             ["choice1","choice2","choice3","choice4"]],
            [["choice1","choice2","choice3","choice4"],
             ["choice1","choice2","choice3","choice4"],
             ["choice1","choice2","choice3","choice4"],
             ["choice1","choice2","choice3","choice4"],
             ["choice1","choice2","choice3","choice4"]]]

#randomized questions version below ----
#populate the questions with the questions from the scraped data, and have it so the questions are randomized if we are pulling more than 25 questions 
# shuffled_list = list(questions_and_choices.items())
# random.shuffle(shuffled_list)
# shuffled_data = dict(shuffled_list)
# questions = list(shuffled_data.keys())
# choices = list(shuffled_data.values())
#----

#oct 31
#questions = list(webscraping_data.keys())
#choices = list(webscraping_data.values())
questions = list()
choices = list()
answers_list = list()
for question, answers in webscraping_data.items():
    questions.append(question)
    choices.append(answers[0])
    if answers[1]:
        answers_list.append(answers[1][0])

print(answers_list)

total_questions = len(questions)

# \\ TODO: shouldnt this check if BUTTONS_PER_LINE*BUTTONS_PER_LINE > total_questions ? Doesn't the counter below account for the correct number of questions?
# Ensure BUTTONS_PER_LINE doesn't exceed the total number of questions, so we always have a 5x5 grid 
if BUTTONS_PER_LINE > total_questions:
    BUTTONS_PER_LINE = total_questions

counter = 0  # counter to make sure each question + choices placeholders are being swapped with the data properly

for i in range(BUTTONS_PER_LINE):
    for j in range(BUTTONS_PER_LINE):
        counter += 1
        if counter < total_questions:
            QUESTIONS[i][j] = questions[counter]
            ANSWER_CHOICES[i][j] = choices[counter]
        else:
            # in case you dont have enough questions, like how the site we are currently scraping from is gettign in 23 questions
            QUESTIONS[i][j] = "No more questions"

NUMBER_ANSWER_CHOICES = 4

counter = 0 
#issue: need to figure out a different way to store the correct answers if implementing the randomized questions version
# nov 2nd update: should be solved?
# \\ TODO: In testing it seems like some questions have no correct answer, maybe this is related to the oct 31 comment below? Printing out answers_liost, it seems like the correct answer for each question is included in the list, but the order is wrong so some questions have no correct answer?

CORRECT_ANSWERS = [[0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0]]

#replace the correct answer placeholders correctly
for i in range(BUTTONS_PER_LINE):
    for j in range(BUTTONS_PER_LINE):
        counter += 1
        CORRECT_ANSWERS[i][j] = answers_list[counter]

counter = 0

#oct 31: need to go through the answer choices and remove all the unncessary ones, not sure why they are showing up.

# Define colors of message to indicate completion status.
BUTTON_COLORS = [[DEFAULT_COLOR, DEFAULT_COLOR, DEFAULT_COLOR, DEFAULT_COLOR, DEFAULT_COLOR],
                 [DEFAULT_COLOR, DEFAULT_COLOR, DEFAULT_COLOR, DEFAULT_COLOR, DEFAULT_COLOR],
                 [DEFAULT_COLOR, DEFAULT_COLOR, DEFAULT_COLOR, DEFAULT_COLOR, DEFAULT_COLOR],
                 [DEFAULT_COLOR, DEFAULT_COLOR, DEFAULT_COLOR, DEFAULT_COLOR, DEFAULT_COLOR],
                 [DEFAULT_COLOR, DEFAULT_COLOR, DEFAULT_COLOR, DEFAULT_COLOR, DEFAULT_COLOR]]

###############################################################################
#    FUNCTIONS:
###############################################################################

def buttonCallback(x_in,y_in,buttons,labels,window):

    for x in range(BUTTONS_PER_LINE):
        labels[x].destroy()
        for y in range(BUTTONS_PER_LINE):
            buttons[x][y].destroy()

    question_label = tk.Label(text=QUESTIONS[x_in][y_in],
                              wraplength=GAME_DIMENSION,
                            font=NORMAL_FONT,
                            bg=BACKGROUND_COLOR,
                            fg=TEXT_COLOR)

    question_label.place(width=GAME_DIMENSION,
                         height=TITLE_SIZE*3,
                         x=0,
                         y=0)

    answer_buttons = [0 for i in range(NUMBER_ANSWER_CHOICES)]

    for i in range(NUMBER_ANSWER_CHOICES):

        answer_buttons[i] = tk.Button(window,
                               text=ANSWER_CHOICES[x_in][y_in][i],
                               wraplength=GAME_DIMENSION,
                               font=NORMAL_FONT,
                               bg=DEFAULT_COLOR,
                               highlightbackground=DEFAULT_COLOR,
                               fg=TEXT_COLOR,
                               command=lambda x_in=x_in, y_in=y_in, i=i: answerCallback(x_in,y_in,i,answer_buttons,window))
        
        answer_buttons[i].place(width=GAME_DIMENSION,
                                height=BUTTON_DIMENSION,
                                x=0,
                                y=i*BUTTON_DIMENSION+BUTTON_DIMENSION)

def answerCallback(x_in,y_in,selection,answer_buttons,window):

    for button in answer_buttons:
        button.destroy()

    #nov 2nd testing
    # print(selection)
    # print(ANSWER_CHOICES[x_in][y_in][selection])
    # print(CORRECT_ANSWERS[x_in][y_in])
    if ANSWER_CHOICES[x_in][y_in][selection] == CORRECT_ANSWERS[x_in][y_in]: # made the correct answer selection work properly nov 2nd
        BUTTON_COLORS[x_in][y_in] = CORRECT_COLOR
    else:
        BUTTON_COLORS[x_in][y_in] = INCORRECT_COLOR

    createMain(window)

def createMain(window):

    # Define a 2D array of buttons.
    buttons = [[0 for x in range(BUTTONS_PER_LINE)] for y in range(BUTTONS_PER_LINE)]

    # Define a 1D array of section labels.
    labels = [0 for x in range(BUTTONS_PER_LINE)]

    # Define a 1x1 pixel used as the button and label background which allows
    # setting the size of the buttons and labels in units of pixels as opposed to
    # units of text font size.

    # Create buttons and labels at each of the desired locations.
    for x in range(BUTTONS_PER_LINE):

        # Create the labels.
        labels[x] = tk.Label(text=LABEL_NAMES[x],
                             wraplength=BUTTON_DIMENSION,
                            font=NORMAL_FONT,
                            bg=BACKGROUND_COLOR,
                            fg=TEXT_COLOR)

        # Place the labels at increasing distance in the x direction.
        labels[x].place(width=BUTTON_DIMENSION,
                        height=TITLE_SIZE,
                        x=x*BUTTON_DIMENSION,
                        y=0)

        for y in range(BUTTONS_PER_LINE):

            # Create the buttons.
            buttons[x][y] = tk.Button(window,
                                    text=BUTTON_NAMES[y],
                                    font=NORMAL_FONT,
                                    bg=BUTTON_COLORS[x][y],
                                    highlightbackground=BUTTON_COLORS[x][y],
                                    fg=TEXT_COLOR,
                                    command=lambda x=x, y=y: buttonCallback(x,y,buttons,labels,window))

            # Place the buttons at increasing distance in the x and y directions.
            buttons[x][y].place(width=BUTTON_DIMENSION,
                                height=BUTTON_DIMENSION,
                                x=x*BUTTON_DIMENSION,
                                y=y*BUTTON_DIMENSION+TITLE_SIZE)

###############################################################################
#    MAIN:
###############################################################################
def main():
    window = tk.Tk()
    window.title("Jeopardy Game")
    window.resizable(False, False) # might have to change this to fix our issue of text not fitting properly

    # # Create the canvas for the game.
    canvas = tk.Canvas(window, bg=BACKGROUND_COLOR, height=GAME_DIMENSION+TITLE_SIZE, width=GAME_DIMENSION)

    # Pack the canvas.
    canvas.pack()

    # Update the game window.
    window.update()

    createMain(window)

    # Run the main loop of the program.
    tk.mainloop()

main()