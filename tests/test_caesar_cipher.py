"""
test_caesar_cipher.py
=====================

Unit tests for the CaesarCrypt project.

These tests check the pure cipher logic in `caesar_cipher.py` using
only Python's built-in `unittest` module (no external libraries).

Run from the project root folder with:

    python -m unittest discover -s tests -v

or:

    python -m unittest tests.test_caesar_cipher -v
"""

import os
import sys
import unittest

# Make the project root importable no matter where the tests are
# launched from (root is the parent folder of the tests/ folder).
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from caesar_cipher import decrypt, encrypt, normalize_shift


class TestEncryption(unittest.TestCase):
    """Tests for the encrypt() function."""

    def test_uppercase_letters(self):
        self.assertEqual(encrypt("ABC", 3), "DEF")
        self.assertEqual(encrypt("HELLO", 3), "KHOOR")

    def test_uppercase_wraps_around(self):
        self.assertEqual(encrypt("XYZ", 3), "ABC")

    def test_lowercase_letters(self):
        self.assertEqual(encrypt("abc", 3), "def")
        self.assertEqual(encrypt("hello", 3), "khoor")

    def test_lowercase_wraps_around(self):
        self.assertEqual(encrypt("xyz", 3), "abc")

    def test_mixed_case(self):
        self.assertEqual(encrypt("Hello World", 3), "Khoor Zruog")

    def test_spaces_preserved(self):
        self.assertEqual(encrypt("Hello World", 3), "Khoor Zruog")

    def test_numbers_preserved(self):
        self.assertEqual(encrypt("Hello123!", 3), "Khoor123!")

    def test_special_characters_preserved(self):
        self.assertEqual(encrypt("Hello!@# ", 5), "Mjqqt!@# ")

    def test_shift_zero(self):
        self.assertEqual(encrypt("Hello World", 0), "Hello World")

    def test_shift_twenty_six(self):
        self.assertEqual(encrypt("Hello World", 26), "Hello World")

    def test_shift_greater_than_26(self):
        self.assertEqual(encrypt("Hello", 29), "Khoor")

    def test_large_positive_shift(self):
        self.assertEqual(encrypt("Hello", 1000), "Tqxxa")

    def test_negative_shift(self):
        self.assertEqual(encrypt("Khoor", -3), "Hello")

    def test_very_large_negative_shift(self):
        self.assertEqual(encrypt("Hello", -26), "Hello")

    def test_empty_text(self):
        self.assertEqual(encrypt("", 5), "")

    def test_non_letter_characters_only(self):
        self.assertEqual(encrypt("123 !@#", 5), "123 !@#")


class TestDecryption(unittest.TestCase):
    """Tests for the decrypt() function."""

    def test_basic_decryption(self):
        self.assertEqual(decrypt("DEF", 3), "ABC")
        self.assertEqual(decrypt("Khoor Zruog", 3), "Hello World")

    def test_decrypt_wraps_around(self):
        self.assertEqual(decrypt("ABC", 3), "XYZ")

    def test_decrypt_with_negative_shift(self):
        self.assertEqual(decrypt("Hello", -3), "Khoor")

    def test_decrypt_with_shift_greater_than_26(self):
        self.assertEqual(decrypt("Khoor", 29), "Hello")

    def test_decrypt_preserves_numbers_and_symbols(self):
        self.assertEqual(decrypt("Khoor123!", 3), "Hello123!")

    def test_decrypt_empty_text(self):
        self.assertEqual(decrypt("", 7), "")


class TestShiftNormalization(unittest.TestCase):
    """Tests for the normalize_shift() helper."""

    def test_normalize_in_range(self):
        self.assertEqual(normalize_shift(3), 3)
        self.assertEqual(normalize_shift(0), 0)

    def test_normalize_above_26(self):
        self.assertEqual(normalize_shift(29), 3)
        self.assertEqual(normalize_shift(26), 0)
        self.assertEqual(normalize_shift(52), 0)

    def test_normalize_negative(self):
        self.assertEqual(normalize_shift(-3), 23)
        self.assertEqual(normalize_shift(-1), 25)

    def test_normalize_rejects_non_integers(self):
        for bad in [2.5, "3", None, True, [3]]:
            with self.assertRaises(ValueError):
                normalize_shift(bad)


class TestRoundTrip(unittest.TestCase):
    """Encryption followed by decryption must recover the original."""

    def test_round_trip_multiple_cases(self):
        cases = [
            ("Hello World", 3),
            ("HELLO", 7),
            ("hello world", 13),
            ("Python 3.11! @home", 25),
            ("  leading and trailing   ", 8),
            ("a", 0),
            ("A1b2C3", 100),
            ("", 12),
        ]
        for text, shift in cases:
            with self.subTest(text=text, shift=shift):
                self.assertEqual(decrypt(encrypt(text, shift), shift), text)


if __name__ == "__main__":
    unittest.main(verbosity=2)