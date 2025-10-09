import pytest

from mastermind import MyMastermind
from unittest.mock import patch

@pytest.mark.parametrize("code, guess, expected_result, difficulty", [
    (["blue","green","pink","orange"], ["pink","green","orange","purple"], (1, 2), ("easy", "no")),
    (["blue","green","pink","orange"], ["green","green","green","purple"], (1, 0), ("easy", "yes")),
])
def test_evaluate_guess(code, guess, expected_result, difficulty):
    """Checks if logic behind the game is correct, does the game give the correct feedback when it comes to position and colour
    expected_result = tuple of 2 integers
    """
    game = MyMastermind(difficulty)
    game.code = code
    evaluation = game.evaluate_guess(guess)

    assert evaluation == expected_result, f"{evaluation} should be {expected_result}"

def duplicate_colour_test():   # test to see how often duplicate colors appear when enabled, does 50 games
    counter = 0
    duplicate = 0

    with patch('builtins.input', side_effect=["yes", "quit"]*50):
        while counter < 50:
            counter +=1
            code = MyMastermind().code
            
            if len(set(code)) < len(code):   # checks if there are duplicate colors in the code
                duplicate += 1

        print (duplicate/50*100)   # percentage of games with duplicate colors