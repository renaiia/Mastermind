import random

class MyMastermind():
    colors = ["pink","orange","yellow","green","blue","purple","white","black"]

    def __init__(self, settings=None):   # initializes the game variables and saves the guesses
        self.previous_guesses = []
        self.settings = self.implement_settings(settings)
        self.code = self.generate_code()

    def start_game(self):   # starts the game
        self.run_game()

    def run_game(self):
        """Runs the game loop, until either the correct guess or a manual quit is enter. Allowed access to previous guesses with history"""

        guess = " "
        
        while guess != self.code and guess[0] != "quit":   # runs the game
            guess = self.get_guess()
            guess = self.guess_decoder(guess)
            guess = self.check_colors(guess) 

            if guess[0] == "history":   # shows the player their previous guesses
                self.ui_responses("history")
                guess = self.get_guess()
            elif guess[0] == "quit":   # enables the player to quit
                self.ui_responses("quit")
            elif guess == self.code:   # checks if the guess is correct
                self.ui_responses("win")
            else:
                pegs = self.evaluate_guess(guess)   # gets number of white and red pegs
                self.previous_guesses.append((guess, pegs))
                self.ui_responses("eval", pegs[0], pegs[1])
    
    def implement_settings(self, settings=None):    # Extra code her 
        """ Sets the difficulty for the game and returns them as a dict"""
        if settings != None:   # for testing purposes
            pass
        else:
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
            "colors": col,
            "pegs": peg
        }

        return settings
        
    def generate_code(self):
        """ Generates the code of the game, return the code as a list"""

        if self.settings["dupes"] == "yes":
            code = random.choices(self.colors[0:self.settings["colors"]], k=self.settings["pegs"])
        elif self.settings["dupes"] == "no":
            code = random.sample(self.colors[0:self.settings["colors"]], k=self.settings["pegs"])
        
        return code

    def evaluate_guess(self, guess):   # compares guess against the code
        """Compares the guess against the code, returns the evaluation as a tuple of 2 integers. 1st white, 2nd red"""

        red = []
        white = []
        code_no_red = []
        guess_no_red = [] 
        
        for g, c in zip(guess, self.code):   # checks colour + placement
            if g == c:
                red.append(g)
            else: 
                code_no_red.append(c)
                guess_no_red.append(g)

        for g in guess_no_red:  # checks colour only
            if g in code_no_red:
                white.append(g), code_no_red.remove(g)

        return len(red), len(white)   # return the number of white and red pegs

    def ui_responses(self, options, red = None, white = None):
        """ handles all user feedback via print statements"""

        col = ', '.join(self.colors[0:self.settings["colors"]])
        pegs = self.settings['pegs']
        

        if options == "win":
            print (f"Correct! The code was: {self.code}")
            print (f"You did it in {len(self.previous_guesses)} attempts")
        elif options == "quit": 
            print (f"The code was: {self.code}")
        elif options == "eval":
            print (f"White:{white} Red:{red}")
            return (f"White:{white} Red:{red}")
        elif options == "colors":
            print(f"Available colors: {col}")
        elif options == "colors error":
            print(f"Guess must be {pegs} of these: {col}")
        elif options == "history":
            for guess in self.previous_guesses:
                print (f"Guess: {guess[0]} Red: {guess[1][0]} White: {guess[1][1]}")

    def guess_decoder(self, guess):   # i choose to to it like this because i want to make a gui later and this will be unnecessary   
        """Takes guess and checks if it is an abbreviation, decodes it and returns the unabbreviated guess as a list"""

        abr_col = {
            "pi": "pink",
            "or": "orange",
            "ye": "yellow",
            "gr": "green",
            "bl": "blue",
            "pu": "purple",
            "wh": "white",
            "bla": "black"
            }
        
        decoded = []

        for g in guess:
            if g not in self.colors:
                try: 
                    decoded.append(abr_col[g])
                except: 
                    decoded.append(g)
            else: 
                decoded.append(g)
        
        return decoded

    def check_length(self, guess):
        """ Makes sure guess matches number of pegs, re asks until it does, and returns the guess as a list"""

        pegs = self.settings["pegs"] 

        while len(guess)!= pegs:
            if guess[0] == "quit" or guess[0] == "history":
                return guess
            guess = input(f"Guess must contain {pegs} colors: ").strip().lower().split()
        
        return guess
    
    def check_colors(self, guess):
        """ Check if guess contains allowed colors, if it does not ask for new guess and calls the check length and decoder functions, before checking again. Returns a valid guess as a list """
        while any(g not in self.colors[0:self.settings["colors"]] for g in guess):   # Makes sure guess only contains possible colors
            if guess[0] == "quit" or guess[0] == "history":
                return guess
            self.ui_responses("colors error")
            guess = input("Place your guess here: ").strip().lower().split()
            guess = self.guess_decoder(guess) 
            guess = self.check_length(guess)
        
        return guess

    def get_guess(self):
        """Gets user guess and checks if user input is valid, return the guess as a list"""
        # change name and validate 
        self.ui_responses("colors")
        guess = input("Place your guess here: ").strip().lower().split()

        if guess[0] == "quit":
            return guess
        
        if guess[0] == "history":
            return guess

        # guess = self.check_length(guess)
        # guess = self.guess_decoder(guess)
        # guess = self.check_colors(guess) 

        return guess
    
    def get_settings(self):
        """Ask for game difficulty and if duplicate colors are allowed. Returns two values. 1st the difficulty, 2nd if dupes allowed"""

        difficulty = input("Choose your difficulty?: ").strip().lower()

        while difficulty != "easy" and difficulty != "medium" and difficulty != "hard" and difficulty != "expert":
            difficulty = input("Please enter easy, medium, hard or expert: ").strip().lower()
        
        dupes = input("Allow duplicate colors?: ").strip().lower()

        while dupes != "yes" and dupes != "no":
            dupes = input("Please enter yes or no: ").strip().lower()

        return difficulty, dupes
    
if __name__ == "__main__": 
    game = MyMastermind()
    game.start_game()
