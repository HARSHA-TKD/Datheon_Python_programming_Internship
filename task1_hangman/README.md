# Hangman Ultimate

A feature-rich, terminal-based word guessing game built with Python.

## Features

- Three difficulty levels: Easy, Medium and Hard
- Four word categories, including Cybersecurity
- Random word selection and clues
- Visual Hangman progression
- Hint system with score penalties
- Score tracking and high-score persistence
- Win-rate statistics
- Input validation and replayable gameplay

## Requirements

- Python 3.8 or later
- No external packages required

## How to Run

From the root of the repository:

```bash
python task1_hangman/hangman.py
```

## How to Run Tests

```bash
python -m unittest discover -s task1_hangman -p "test_*.py" -v
```

## Project Structure

```text
task1_hangman/
├── hangman.py
├── test_hangman.py
└── README.md
```

## Concepts Practiced

- Functions and loops
- Dictionaries, lists and sets
- Conditional statements
- Exception handling
- JSON file handling
- Automated testing with unittest

## Future Improvements

- Add a graphical user interface
- Add more word categories
- Introduce a timed game modes