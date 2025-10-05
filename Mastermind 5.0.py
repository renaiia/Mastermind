import random
from unittest.mock import patch

"""
This is a mastermind. The player has to guess a sequence of 4 colours form a list of 6 in easy mode.
The player can choose if duplicate colours are allowed and between 4 difficulties.
The player gets feedback via a red or white pegs. Red = right collour and place, White = right collour but wrong place.

I have added comments to explain the code 
I have chosen to sepearte all user input and feedsback from the game logic allow for expansion later if i want to add a GUI or AI player.
"""
# give function """ """ dockstings
class MyMastermind:
    colours = ["pink","orange","yellow","green","blue","purple","white","black"]

    def __init__(self):   # initialises the game variables and saves the guesses
        self.previous_guesses = []
        self.settings = self.implement_settings()
        self.code = self.generate_code()

    def start_game(self):   # starts the game
        self.run_game()

    def run_game(self):   # runs the game loop
        guess = " "
        
        while guess != self.code and guess[0] != "quit":   # runs the game
            guess = self.get_guess()

            if guess[0] == "history":   # shows the player their previous guesses
                self.ui_responses("history")
                guess = self.get_guess()
            elif guess[0] == "quit":   # enables the player to quit
                self.ui_responses("quit")
            elif guess == self.code:   # checks if the guess is correct
                self.ui_responses("win")
            else:
                pegs = self.check_against_code(guess)   # gets number of white and red pegs
                self.previous_guesses.append((guess, pegs))
                self.ui_responses("eval", pegs[0], pegs[1])
    
    def implement_settings(self):   # sets the difficulty for the game
        settings = self.get_settings()

        if settings[0] == "easy":
            col = 6 
            peg = 4
        elif settings[0] == "medium":
            col = 8 
            peg = 4
        elif settings[0] == "hard":
            col = 8
            peg = 5
        elif settings[0] == "expert":
            col = 8
            peg = 6
        
        settings = {
            "difficulty": settings[0],
            "dupes": settings[1],
            "colours": col,
            "pegs": peg
        }

        return settings
        
    def generate_code(self):   # generates the code for the game
        if self.settings["dupes"] == "yes":
            code = random.choices(self.colours[0:self.settings["colours"]], k=self.settings["pegs"])
        elif self.settings["dupes"] == "no":
            code = random.sample(self.colours[0:self.settings["colours"]], k=self.settings["pegs"])
        
        return code

    def check_against_code(self, guess):   # compares guess against the code
        white = []
        red = []
        code_no_red = []
        guess_no_red = [] 
        
        for g, c in zip(guess, self.code):   # checks collour + placement
            if g == c:
                red.append(g)
            else: 
                code_no_red.append(c)
                guess_no_red.append(g)

        for g in guess_no_red:  # checks collour only
            if g in code_no_red:
                white.append(g), code_no_red.remove(g)

        return len(white), len(red)   # return the number of white and red pegs

    def ui_responses(self, options, white = [], red = []):   # handles all user feedback
        col = ', '.join(self.colours[0:self.settings["colours"]])
        pegs = self.settings['pegs']
        

        if options == "win":
            print (f"Correct! The code was: {self.code}")
            print (f"You did it in {len(self.previous_guesses)} attempts")
        elif options == "quit": 
            print (f"The code was: {self.code}")
        elif options == "eval":
            print (f"White:{white} Red:{red}")
            return (f"White:{white} Red:{red}")
        elif options == "colours":
            print(f"Available colours: {col}")
        elif options == "colours error":
            print(f"Guess must be {pegs} of these: {col}")
        elif options == "history":
            for guess in self.previous_guesses:
                print (f"Guess: {guess[0]} White: {guess[1][0]} Red: {guess[1][1]}")

    def get_guess(self):   # Gets user guess and cheks if user input is valid
        self.ui_responses("colours")
        guess = input("Place your guess here: ").split()
        pegs = self.settings["pegs"] 

        if guess[0] == "quit":
            return guess
        
        if guess[0] == "history":
            return guess

        while len(guess)!= self.settings["pegs"]:   # Makes sure guess matches number of pegs
            guess = input(f"Guess must contain {pegs} colours: ").split()

        while any(g not in self.colours[0:self.settings["colours"]] for g in guess):   # Makes sure guess only contains possible collours
            self.ui_responses("colours error")
            guess = input("Place your guess here: ").split()

        return guess
    
    def get_settings(self):   # ask for game difficulty and if duplicate colours are allowed
        difficulty = input("Choose your dificulty?: ")

        while difficulty != "easy" and difficulty != "medium" and difficulty != "hard" and difficulty != "expert":
            difficulty = input("Please enter easy, medium, hard or expert: ")
        
        dupes = input("Allow duplicate colours?: ")

        while dupes!= "yes" and dupes != "no":
            dupes = input("Please enter yes or no: ")

        return difficulty, dupes
    
# if __name__ == "__main__": 
#     game = MyMastermind()
#     game.start_game()

# MyMastermind().start_game()

"""
I am testing my functions here
"""

def test_check_agienst_code(code, guess):
    MyMastermind().check_against_code(guess)





def duplicate_collour_test():   # test to see how often duplicate colours appear when enabled, does 50 games
    counter = 0
    duplicate = 0

    with patch('builtins.input', side_effect=["yes", "quit"]*50):
        while counter < 50:
            counter +=1
            code = MyMastermind().code
            
            if len(set(code)) < len(code):   # checks if there are duplicate colours in the code
                duplicate += 1

        print (duplicate/50*100)   # percentage of games with duplicate colours
