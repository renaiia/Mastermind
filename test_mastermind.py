import pytest
from mastermind import MyMastermind, get_settings, start_game
from unittest.mock import patch

@pytest.mark.parametrize("code, guess, expected_result", [
    (["cyan","cyan","cyan","cyan"], ["cyan","cyan","cyan","cyan"], (4, 0)),
    (["cyan","cyan","cyan","cyan"], ["pink","pink","pink","pink"], (0, 0)),
    (["cyan","green","pink","orange"], ["green","cyan","orange","pink"], (0, 4)),
    (["cyan","green","pink","orange"], ["green","green","green","purple"], (1, 0)),
    (["cyan","cyan","pink","orange"], ["yellow","pink","green","purple"], (0, 1)),
    (["cyan","green","pink","orange"], ["pink","green","orange","purple"], (1, 2)),
    (["purple","yellow","pink","purple"], ["yellow","green","pink","purple"], (2, 1)),
])
def test_evaluate_guess(code, guess, expected_result):
    game = MyMastermind()
    game.code = code
    evaluation = game.evaluate_guess(guess)

    assert evaluation == expected_result, f"{evaluation} should be {expected_result}"

@pytest.mark.parametrize("settings, pegs, col, eval", [
    (("easy", "no"), 4, 6, True),
    (("easy", "yes"), 4, 6, True),
    (("medium", "no"), 4, 8, True),
    (("medium", "yes"), 4, 8, True),
    (("hard", "no"), 5, 8, True),
    (("hard", "yes"), 5, 8, True),
    (("expert", "no"), 6, 8, True),
    (("expert", "yes"), 6, 8, True),
])
def test_generate_code(settings, pegs, col, eval):
    game = MyMastermind(settings)
    code = game.code
    test = True
    
    assert len(code) == pegs, "Generated wrong number of pegs"

    assert all(c in game.colors[:col] for c in code), "Used color outside allowed range"

    assert len(code) == pegs, "Generated wrong number of pegs"
    
    if settings[1] == "no": 
        assert len(set(code)) == pegs, "Duplicates not allowed but found"

    if settings[1] == "yes" and len(set(code)) != pegs:   # Notifies if duplicates generate when allowed
        print ("True: Generated multiple colors")

@pytest.mark.parametrize("settings, pegs, col, eval", [
    (("easy", "no"), 4, 6, True),
    (("easy", "yes"), 4, 6, True),
    (("medium", "no"), 4, 8, True),
    (("medium", "yes"), 4, 8, True),
    (("hard", "no"), 5, 8, True),
    (("hard", "yes"), 5, 8, True),
    (("expert", "no"), 6, 8, True),
    (("expert", "yes"), 6, 8, True),
])
def test_implement_settings(settings, pegs, col, eval): 
    game = MyMastermind(settings)
    test = True

    if game.settings["colors"] != col:
        test = False
        assert test == eval, "Number of colors dont match"
    if game.settings["pegs"] != pegs:
        test = False
        assert test == eval, "Number of pegs dont match"


def test_initial_guesses():
    with patch('builtins.input', side_effect=["easy", "no", "cy pi gr or", "history", "quit"]), \
         patch('builtins.print') as mock_print:

        settings = get_settings()
        game = MyMastermind(settings)
        start_game(game)

    # Show all print() output
    for call in mock_print.call_args_list:
        printed_output = ' '.join(str(arg) for arg in call[0])
        print("PRINTED:", printed_output)