import random

class MyMastermind():
    colors = ["pink","orange","yellow","green","cyan","purple","white","black"]

    def __init__(self, settings=None):
        """Initialize the game with the given settings.

        Args:
            settings (list[str] or None): Difficulty and dupes e.g. ["easy", "yes"].

        Attributes:
            previous_guesses (list): Stores previous player guesses and results.
            settings (dict): Contains game difficulty, allowed colors, nr of pegs and if duplicates allowed.
            code (list): The code to guess.
        """
        self.previous_guesses = []
        self.settings = self.implement_settings(settings)
        self.code = self.generate_code()

    def implement_settings(self, settings):
        """ Sets the difficulty for the game and returns them as a dict.

        Args:
            settings (list[str] or None): Difficulty and dupes e.g. ["easy", "yes"].

        Returns:
            settings (dict): Contains difficulty(str), dupes(str), colors(int), pegs(int).
        """
        if settings is None:   # enables testing
            return settings

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
        """ Generates random code based on settings.

        Returns:
            code (list[str]): Generated code.
        """
        if self.settings is None:   # enables testing
            return None 

        if self.settings["dupes"] == "yes":
            code = random.choices(self.colors[0:self.settings["colors"]], k=self.settings["pegs"])
        elif self.settings["dupes"] == "no":
            code = random.sample(self.colors[0:self.settings["colors"]], k=self.settings["pegs"])
        
        return code

    def evaluate_guess(self, guess):
        """Compares the guess to the code.

        Args: 
            guess (list[str]): Users guess.

        Returns: 
            tuple (int, int): (red pegs, white pegs).
        """
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

        return len(red), len(white)

def start_game(game, ui_config):
    """Starts the game.
    
    Args:
        game (MyMastermind): Instance of MyMastermind class.
    """
    run_game(game, ui_config)

def run_game(game, ui_config):
    """Runs the game loop, until correct guess or manual quit. Allows access to previous guesses.
    
    Args:
        game (MyMastermind): Instance of MyMastermind class.
    """
    guess = " "
        
    while guess != game.code and guess[0] != "quit":   # runs the game
        guess = get_guess(game, ui_config) 

        if guess[0] == "history":   # shows the player their previous guesses
            ui_responses(game, "history", ui_config)
            guess = get_guess(game, ui_config)
        elif guess[0] == "quit":   # enables the player to quit
            ui_responses(game, "quit", ui_config)
        elif guess == game.code:   # checks if the guess is correct
            ui_responses(game,"win", ui_config)
        else:
            pegs = game.evaluate_guess(guess)   # gets number of white and red pegs
            game.previous_guesses.append((guess, pegs))
            ui_responses(game, "eval", ui_config, pegs[0], pegs[1])

"""UI helpers"""

abr_col = {
        "pi": ("pink"),
        "or": ("orange"),
        "ye": ("yellow"),
        "gr": ("green"),
        "cy": ("cyan"),
        "pu": ("purple"),
        "wh": ("white"),
        "bl": ("black"),
        "re": ("red"),
        }

col_map = {
    "pink": "1;35",
    "orange": "31",
    "yellow": "1;33",
    "green": "1;32",
    "cyan": "1;36",
    "purple": "35",
    "white": "1;37",
    "black": "1;30",
    "red": "1;31"
}

def guess_decoder(game, guess):
    """Checks if guess is an abbreviation and decodes if it is.

    Returns:
        decoded (list[str]): Unabbreviated guess.
    """
    decoded = []

    for g in guess:
        if g not in game.colors:
            try: 
                decoded.append(abr_col[g])
            except: 
                decoded.append(g)
        else: 
            decoded.append(g)
    
    return decoded

"""UI layer"""
def ui_responses(game, options, ui_config, red = None, white = None):
    """ Handles all user feedback via print statements.

    Args:
        options (str): Decides which response to run.
        red (int): Number of red pegs.
        white (int): Number of white pegs.
        game (MyMastermind): Instance of MyMastermind class.
    """ 
    if options == "win":
        print (f"Correct! The code was: {add_colors(game.code, ui_config)}")
        print (f"You did it in {len(game.previous_guesses)} attempts")
    elif options == "quit": 
        print (f"The code was: {add_colors(game.code, ui_config)}")
    elif options == "eval":
        col_red = add_colors(("red", "white"), ui_config)
        print (f"{col_red[0]}:{red} {col_red[1]}:{white}")
        return (f"{col_red[0]}:{red} {col_red[1]}:{white}")
    elif options == "colors":   # choose to not add colored text here
        print(f"Available colors: {', '.join(game.colors[:game.settings['colors']])}")
    elif options == "colors error":
        print(f"Guess must be {game.settings['pegs']} of these: {', '.join(game.colors)}")
    elif options == "history":
        count = 0
        for guess in game.previous_guesses:
            count += 1
            print (f"Guess {count}: {add_colors(guess[0], ui_config)} ⏐ {add_colors('red', ui_config)}: {guess[1][0]} {add_colors('white', ui_config)}: {guess[1][1]}")

def get_settings():   # sends to game logic
    """Asks for game difficulty and if duplicate colors are allowed. 

    Returns:
        tuple (str, str): Difficulty and dupes, e.g. ("easy", "yes").
        """
    difficulty = input("Choose your difficulty?: ").strip().lower()

    while difficulty not in ("easy","medium","hard","expert"):
        difficulty = input("Please enter easy, medium, hard or expert: ").strip().lower()
    
    dupes = input("Allow duplicate colors?: ").strip().lower()

    while dupes != "yes" and dupes != "no":
        dupes = input("Please enter yes or no: ").strip().lower()

    return difficulty, dupes

def get_ui_config():
    """Asks if terminal colors should be used. 

    Returns:
        tuple (str): Difficulty and dupes, e.g. ("yes").
        """
    colors = input("Use colors in terminal?: ")
    
    while colors != "yes" and colors != "no":
        colors = input("Please enter yes or no: ").strip().lower()
    
    if colors == "no":
        colors = False

    return colors

def get_guess(game, ui_config):
    """ Get guess, calls check_length and guess_decoder, runs until guess only contains allowed colors.

    Args:
        game (MyMastermind): Instance of MyMastermind class.

    Returns: 
        guess (list): Valid guess
    """
    ui_responses(game,"colors", ui_config)
    guess = input("Place your guess here: ").strip().lower().split()

    pegs = game.settings["pegs"]

    while True: 
        if guess[0] == "quit" or guess[0] == "history":
            return guess 
        
        if len(guess) == pegs:
            guess = guess_decoder(game, guess)
            if all(g in game.colors[0:game.settings["colors"]] for g in guess):
                return guess
            else:
                ui_responses(game, "colors error", ui_config)
                guess = input("Place your guess here: ").strip().lower().split()
        else: 
            guess = input(f"Guess must contain {pegs} colors: ").strip().lower().split()

def add_colors(text, enabled):
    """Adds ANSI colors to text.

    Args:
        game (MyMastermind): A game instance.

    Returns: 
        Input but colored.
    """
    if enabled == False:
        return text

    colored_list = []

    if type (text) == str:
        return (f"\033[{col_map[text]}m{text}\033[0m")

    for item in text:
        colored_list.append(f"\033[{col_map[item]}m{item}\033[0m")
    
    if len (colored_list) > 2:
        return " ".join(colored_list)
        
    return colored_list

if __name__ == "__main__":   # connects ui and logic
    settings = get_settings()
    ui_config = get_ui_config()
    game = MyMastermind(settings)
    start_game(game, ui_config)