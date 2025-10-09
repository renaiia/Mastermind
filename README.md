# Mastermind
A text based Python mastermind game

## Description
This is a text-based Mastermind game where the player has to guess the hidden color code.

The project demonstrates:
- Python OOP (class-based design)
- Separation of game logic and user interface
- Unit testing with pytest
- Input validation and error handling

## Features
- Four difficulty levels: Easy, Medium, Hard, Expert
- Option to allow or disallow duplicate colors for each difficulty
- Feedback via "red" and "white" pegs:
    - Red = correct color in correct position
    - White = correct color in wrong position
- Tracks guess history, accessed by typing "history"
- Abbreviations supported for colors (first 2 letters, except "black" uses 3, e.g., pi for pink)
- Allows manual quitting by typing "quit"

## Example Gameplay
Choose your difficulty?: easy
Allow duplicate colors?: no
Available colors: pink, orange, yellow, green, blue, purple
Place your guess here: pi or ye gr
White:1 Red:2

## Testing 
Unit tests are included using pytest.

## Future improvements
- Add a cap to number of turns 
- Configurable color sets
- Graphical user interface (GUI) version