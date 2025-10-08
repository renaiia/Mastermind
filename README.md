# Mastermind
A text based mastermind game

Takes user input 
The player has to guess a sequence of 4 colors form a list of 6 in easy mode.
The player can choose if duplicate colors are allowed and between 4 difficulties.
The player gets feedback via a red or white pegs. Red = right color and place, White = right color but wrong place.

I have added comments to explain the code 
I have chosen to separate all user input and feedback from the game logic allow for expansion later if i want to add a GUI or AI player.
"""
It sets up a Mastermind game where a secret color code is generated based on difficulty and whether duplicate colors are allowed.

The player guesses the color code and receives feedback in terms of:

Red pegs = correct color in the correct position

White pegs = correct color in the wrong position

It supports multiple difficulties, each affecting how many colors and pegs are used.

It allows commands like "quit" to exit and "history" to see previous guesses.

It accepts abbreviated color inputs and decodes them to full names.