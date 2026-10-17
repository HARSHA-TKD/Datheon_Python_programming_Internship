import random
import json
import os

# ==========================================
# HANGMAN ULTIMATE - PYTHON EDITION
# ==========================================

TITLE = r"""
 _   _   ___   _   _   ____   __  __   ___   _   _
| | | | / _ \ | \ | | / ___| |  \/  | / _ \ | \ | |
| |_| || | | ||  \| || |  _  | |\/| || | | ||  \| |
|  _  || |_| || |\  || |_| || |  | || |_| || |\  |
|_| |_| \___/ |_| \_| \____| |_|  |_| \___/ |_| \_|
                 ULTIMATE EDITION
"""

HANGMAN_PICTURES = [
    """
     +---+
     |   |
         |
         |
         |
    =======
    """,
    """
     +---+
     |   |
     O   |
         |
         |
    =======
    """,
    """
     +---+
     |   |
     O   |
     |   |
         |
    =======
    """,
    """
     +---+
     |   |
     O   |
    /|   |
         |
    =======
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
    =======
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
    =======
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
    =======
    """
]

CATEGORIES = {
    "1": {
        "name": "Programming",
        "words": [
            ("python", "A popular programming language"),
            ("compiler", "Translates source code"),
            ("variable", "Stores a value in a program"),
            ("function", "Reusable block of code"),
            ("algorithm", "Steps to solve a problem"),
            ("database", "Stores organized information")
        ]
    },
    "2": {
        "name": "Cybersecurity",
        "words": [
            ("firewall", "Filters network traffic"),
            ("encryption", "Protects information by transforming it"),
            ("phishing", "A deceptive attempt to steal information"),
            ("malware", "Software designed to cause harm"),
            ("password", "A secret used to authenticate"),
            ("network", "Connected devices that communicate")
        ]
    },
    "3": {
        "name": "Technology",
        "words": [
            ("keyboard", "Used to type on a computer"),
            ("processor", "Executes computer instructions"),
            ("internet", "A global network of networks"),
            ("database", "Organized digital information"),
            ("software", "Programs that run on a computer"),
            ("satellite", "An object orbiting a planet")
        ]
    },
    "4": {
        "name": "Science",
        "words": [
            ("gravity", "Attraction between objects with mass"),
            ("molecule", "Two or more atoms bonded together"),
            ("telescope", "Helps us observe distant objects"),
            ("electricity", "Energy associated with electric charge"),
            ("ecosystem", "Living things and their environment"),
            ("planet", "A large body orbiting a star")
        ]
    }
}

DIFFICULTIES = {
    "1": {"name": "Easy", "attempts": 8, "hints": 3, "points": 10},
    "2": {"name": "Medium", "attempts": 6, "hints": 2, "points": 20},
    "3": {"name": "Hard", "attempts": 5, "hints": 1, "points": 30}
}

SAVE_FILE = "hangman_scores.json"


def load_scores():
    """Load saved statistics from a JSON file."""
    if not os.path.exists(SAVE_FILE):
        return {"best_score": 0, "games_won": 0, "games_played": 0}

    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Invalid save data")

        return {
            "best_score": max(0, int(data.get("best_score", 0))),
            "games_won": max(0, int(data.get("games_won", 0))),
            "games_played": max(0, int(data.get("games_played", 0)))
        }

    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        print("Warning: Could not read saved scores. Starting fresh.")
        return {"best_score": 0, "games_won": 0, "games_played": 0}


def save_scores(scores):
    """Save statistics so they remain available next time."""
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as file:
            json.dump(scores, file, indent=4)
    except OSError:
        print("Warning: Your scores could not be saved.")


def choose_difficulty():
    print("\nCHOOSE YOUR DIFFICULTY")
    print("1. Easy   - 8 attempts, 3 hints")
    print("2. Medium - 6 attempts, 2 hints")
    print("3. Hard   - 5 attempts, 1 hint")

    while True:
        choice = input("Select difficulty (1-3): ").strip()

        if choice in DIFFICULTIES:
            return DIFFICULTIES[choice]

        print("Invalid choice. Enter 1, 2 or 3.")


def choose_category():
    print("\nCHOOSE YOUR CATEGORY")

    for key, category in CATEGORIES.items():
        print(f"{key}. {category['name']}")

    print("5. Mixed categories")

    while True:
        choice = input("Select category (1-5): ").strip()

        if choice in CATEGORIES:
            return CATEGORIES[choice]["name"], CATEGORIES[choice]["words"]

        if choice == "5":
            all_words = []

            for category in CATEGORIES.values():
                all_words.extend(category["words"])

            return "Mixed", all_words

        print("Invalid choice. Enter a number from 1 to 5.")


def display_word(word, guessed_letters):
    """Show guessed letters and hide the rest."""
    return " ".join(
        letter.upper() if letter in guessed_letters else "_"
        for letter in word
    )


def give_hint(word, guessed_letters):
    """Reveal one unguessed letter."""
    available_letters = [
        letter for letter in word
        if letter not in guessed_letters
    ]

    if not available_letters:
        return None

    return random.choice(available_letters)


def play_game(scores):
    difficulty = choose_difficulty()
    category_name, word_list = choose_category()

    word, clue = random.choice(word_list)
    guessed_letters = set()
    wrong_guesses = set()

    attempts_left = difficulty["attempts"]
    hints_left = difficulty["hints"]
    score = 0

    print("\n" + "=" * 45)
    print(f"CATEGORY: {category_name.upper()}")
    print(f"DIFFICULTY: {difficulty['name'].upper()}")
    print(f"CLUE: {clue}")
    print("=" * 45)

    while attempts_left > 0:
        picture_index = (
            difficulty["attempts"] - attempts_left
        )
        picture_index = round(
            picture_index * 6 / difficulty["attempts"]
        )

        print(HANGMAN_PICTURES[picture_index])
        print("Word:", display_word(word, guessed_letters))
        print("Wrong letters:", " ".join(sorted(wrong_guesses)) or "None")
        print(f"Attempts remaining: {attempts_left}")
        print(f"Hints remaining: {hints_left}")
        print(f"Current score: {score}")

        if all(letter in guessed_letters for letter in word):
            break

        print("\nEnter a letter, type H for a hint, or type 0 to quit.")
        guess = input("Your choice: ").strip().lower()

        if guess == "0":
            print(f"\nYou left the game. The word was: {word.upper()}")
            return

        if guess == "h":
            if hints_left > 0:
                hint_letter = give_hint(word, guessed_letters)

                if hint_letter is not None:
                    guessed_letters.add(hint_letter)
                    hints_left -= 1
                    score = max(0, score - 5)
                    print(f"Hint revealed: {hint_letter.upper()}")
                else:
                    print("There are no hidden letters left.")
            else:
                print("You have no hints remaining.")

            continue

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter exactly one alphabetic letter.")
            continue

        if guess in guessed_letters or guess in wrong_guesses:
            print("You already tried that letter!")
            continue

        if guess in word:
            guessed_letters.add(guess)
            score += difficulty["points"]
            print("Correct! Great guess!")

        else:
            wrong_guesses.add(guess)
            attempts_left -= 1
            score = max(0, score - 3)
            print("Wrong guess! Keep trying.")

        if all(letter in guessed_letters for letter in word):
            break

    scores["games_played"] += 1

    if all(letter in guessed_letters for letter in word):
        bonus = attempts_left * 5
        score += bonus

        print(HANGMAN_PICTURES[0])
        print("\nYOU WIN! Congratulations!")
        print("The word was:", word.upper())
        print("Remaining-attempt bonus:", bonus)
        print("Final score:", score)

        scores["games_won"] += 1

        if score > scores["best_score"]:
            scores["best_score"] = score
            print("NEW HIGH SCORE!")

    else:
        print(HANGMAN_PICTURES[6])
        print("\nGAME OVER!")
        print("The correct word was:", word.upper())
        print("Final score:", score)

    save_scores(scores)


def main():
    scores = load_scores()

    print(TITLE)
    print("Welcome to Hangman Ultimate!")
    print("Guess words, earn points and beat your record.")

    while True:
        print("\n" + "-" * 35)
        print("1. Play game")
        print("2. View statistics")
        print("3. Exit")

        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            play_game(scores)

        elif choice == "2":
            print("\nYOUR STATISTICS")
            print("Games played:", scores["games_played"])
            print("Games won:", scores["games_won"])
            print("Best score:", scores["best_score"])

            if scores["games_played"] > 0:
                win_rate = (
                    scores["games_won"] / scores["games_played"]
                ) * 100
                print(f"Win rate: {win_rate:.1f}%")
            else:
                print("Win rate: 0.0%")

        elif choice == "3":
            save_scores(scores)
            print("Thanks for playing Hangman Ultimate!")
            print("See you next time!")
            break

        else:
            print("Invalid choice. Enter 1, 2 or 3.")


if __name__ == "__main__":
    main()