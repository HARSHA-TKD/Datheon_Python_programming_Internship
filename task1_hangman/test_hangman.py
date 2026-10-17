import unittest
import hangman


class TestHangman(unittest.TestCase):

    def test_display_word_hides_letters(self):
        result = hangman.display_word("python", {"p", "o"})
        self.assertEqual(result, "P _ _ _ O _")

    def test_display_word_reveals_all_letters(self):
        result = hangman.display_word("cat", {"c", "a", "t"})
        self.assertEqual(result, "C A T")

    def test_hint_reveals_hidden_letter(self):
        word = "python"
        guessed = {"p", "y", "t", "h", "o"}
        hint = hangman.give_hint(word, guessed)
        self.assertEqual(hint, "n")

    def test_hint_returns_none_when_word_is_complete(self):
        result = hangman.give_hint("cat", {"c", "a", "t"})
        self.assertIsNone(result)

    def test_hint_does_not_reveal_guessed_letters(self):
        word = "banana"
        guessed = {"b", "a"}
        hint = hangman.give_hint(word, guessed)
        self.assertIn(hint, {"n"})

    def test_categories_are_available(self):
        self.assertEqual(len(hangman.CATEGORIES), 4)
        self.assertIn("Programming", [
            category["name"]
            for category in hangman.CATEGORIES.values()
        ])


if __name__ == "__main__":
    unittest.main()