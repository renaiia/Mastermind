import pytest
from mastermind import MyMastermind

@pytest.mark.parametrize("code, guess, expected_result", [
    (["blue","blue","blue","blue"], ["blue","blue","blue","blue"], (4, 0)),
    (["blue","blue","blue","blue"], ["pink","pink","pink","pink"], (0, 0)),
    (["blue","green","pink","orange"], ["green","blue","orange","pink"], (0, 4)),
    (["blue","green","pink","orange"], ["green","green","green","purple"], (1, 0)),
    (["blue","blue","pink","orange"], ["yellow","pink","green","purple"], (0, 1)),
    (["blue","green","pink","orange"], ["pink","green","orange","purple"], (1, 2)),
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