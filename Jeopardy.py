import time
import tkinter as tk # Used to create game interface.
from tkinter import messagebox
from bs4 import BeautifulSoup

###############################################################################
#    CONSTANTS:
###############################################################################

GAME_DIMENSION = 700
BUTTONS_PER_LINE = 5
BUTTON_DIMENSION = int(GAME_DIMENSION/BUTTONS_PER_LINE)
TITLE_SIZE = 50

BACKGROUND_COLOR = "white"
TEXT_COLOR = "black"

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

# Define messages to be presented when each button is clicked.
MESSAGES = [['Message 1',
             'Message 2',
             'Message 3',
             'Message 4',
             'Message 5'],
            ['Message 6',
             'Message 7',
             'Message 8',
             'Message 9',
             'Message 10'],
            ['Message 11',
             'Message 12',
             'Message 13',
             'Message 14',
             'Message 15'],
            ['Message 16',
             'Message 17',
             'Message 18',
             'Message 19',
             'Message 20'],
            ['Message 21',
             'Message 22',
             'Message 23',
             'Message 24',
             'Message 25']]

###############################################################################
#    FUNCTIONS:
###############################################################################

def buttonCallback(x_in,y_in):
    messagebox.showinfo("Message", MESSAGES[x_in][y_in])

###############################################################################
#    MAIN:
###############################################################################

window = tk.Tk()
window.title("Jeopardy Game")
window.resizable(False, False)

# Create the canvas for the game.
canvas = tk.Canvas(window, bg=BACKGROUND_COLOR, height=GAME_DIMENSION+TITLE_SIZE, width=GAME_DIMENSION)

# Pack the canvas.
canvas.pack()

# Update the game window.
window.update()

# Find the width of our window and monitor.
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate the center of the screen.
screen_center_x = (screen_width//2) - (window_width//2)
screen_center_y = (screen_height//2) - (window_height//2)

# Sets the dimension of the window within the computer screen.
window.geometry(f"{window_width}x{window_height}+{screen_center_x}+{screen_center_y}")

# Define a 2D array of buttons.
buttons = [[0 for x in range(BUTTONS_PER_LINE)] for y in range(BUTTONS_PER_LINE)]

# Define a 1D array of section labels.
labels = [0 for x in range(BUTTONS_PER_LINE)]

# Define a 1x1 pixel used as the button and label background which allows
# setting the size of the buttons and labels in units of pixels as opposed to
# units of text font size.
button_image = tk.PhotoImage(width=1, height=1)

# Create buttons and labels at each of the desired locations.
for x in range(BUTTONS_PER_LINE):

    # Create the labels.
    labels[x] = tk.Label(text=LABEL_NAMES[x],
                         compound='left',
                         image=button_image,
                         font=NORMAL_FONT,
                         bg=BACKGROUND_COLOR,
                         fg=TEXT_COLOR,
                         height=TITLE_SIZE,
                         width=BUTTON_DIMENSION)

    # Place the labels at increasing distance in the x direction.
    labels[x].place(x=x*BUTTON_DIMENSION, y=0)

    for y in range(BUTTONS_PER_LINE):

        # Create the buttons.
        buttons[x][y] = tk.Button(window,
                                  text=BUTTON_NAMES[y],
                                  compound='left',
                                  image=button_image,
                                  font=NORMAL_FONT,
                                  bg=BACKGROUND_COLOR,
                                  fg=TEXT_COLOR,
                                  height=BUTTON_DIMENSION,
                                  width=BUTTON_DIMENSION,
                                  command=lambda x=x, y=y: buttonCallback(x,y))

        # Place the buttons at increasing distance in the x and y directions.
        buttons[x][y].place(x=x*BUTTON_DIMENSION,y=y*BUTTON_DIMENSION+TITLE_SIZE)

# Run the main loop of the program.
tk.mainloop()
