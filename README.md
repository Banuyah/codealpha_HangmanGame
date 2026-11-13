# CodeAlpha Hangman Game

A beginner-friendly graphical Hangman game built with Python and Tkinter.

## Features
- Category selection screen with 30 categories
- 20 words per category (600 word entries)
- Random word selection
- A-Z letter buttons
- Six incorrect guesses maximum
- Hangman drawing updates after incorrect guesses
- Optional hint button (only displays a hint when requested)
- Score counter
- Play Again and category navigation

## Requirements
- Python 3.9 or later
- Tkinter (normally included with standard Python installations)

## Run
```bash
python hangman.py
```

If `python` does not work on Windows:
```bash
py hangman.py
```

## Files
- `hangman.py`: Tkinter game interface and game logic
- `categories.py`: category names and word lists
- `requirements.txt`: dependency note

## Note
The word lists are predefined in `categories.py`. No user word entry, internet connection, or external package is required.
