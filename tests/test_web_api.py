"""
test_web_api.py
===============

Optional integration tests for the FastAPI web version (web/api/index.py).

These tests exercise the form handler and the JSON API validation only -
no live HTTP server is needed. They are auto-skipped when FastAPI/Pydantic
are not installed (which keeps the CLI test suite dependency-free):

    python -m unittest discover -s tests -v
"""

import os
import sys
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    # Mirror the deploy layout: `web/` is on sys.path so the import
    # resolves to web/caesar_cipher.py (the self-contained web copy).
    sys.path.insert(0, os.path.join(PROJECT_ROOT, "web"))
    from api import index as web_index
    from fastapi import HTTPException
except ImportError:
    web_index = None
    HTTPException = None


@unittest.skipUnless(web_index is not None, "FastAPI/Pydantic not installed - skipping web tests")
class TestWebForm(unittest.TestCase):
    """Tests for the HTML form handler (handle_form)."""

    def test_form_preserves_leading_and_trailing_spaces(self):
        html = web_index.handle_form("  Hello  ", "3", "encrypt")
        self.assertIn("  Hello  ", html)
        self.assertIn("  Khoor  ", html)

    def test_form_encrypts(self):
        html = web_index.handle_form("Hello World", "3", "encrypt")
        self.assertIn("Khoor Zruog", html)

    def test_form_decrypts(self):
        html = web_index.handle_form("Khoor Zruog", "3", "decrypt")
        self.assertIn("Hello World", html)

    def test_form_invalid_mode_reports_error(self):
        html = web_index.handle_form("Hello", "3", "unknown")
        self.assertIn("Invalid mode", html)
        self.assertNotIn("Khoor", html)

    def test_form_empty_text_reports_error(self):
        html = web_index.handle_form("   ", "3", "encrypt")
        self.assertIn("cannot be empty", html)

    def test_form_invalid_shift_reports_error(self):
        html = web_index.handle_form("Hello", "abc", "encrypt")
        self.assertIn("Invalid shift key", html)

    def test_form_shows_normalization_note(self):
        html = web_index.handle_form("Hello", "29", "encrypt")
        self.assertIn("29 normalized to 3", html)


@unittest.skipUnless(web_index is not None, "FastAPI/Pydantic not installed - skipping web tests")
class TestWebApi(unittest.TestCase):
    """Tests for the JSON API core function (run_cipher)."""

    def test_encrypt(self):
        payload = web_index.run_cipher("encrypt", "Hello World", 3)
        self.assertEqual(payload["result"], "Khoor Zruog")
        self.assertEqual(payload["shift"], 3)

    def test_decrypt(self):
        payload = web_index.run_cipher("decrypt", "Khoor Zruog", 29)
        self.assertEqual(payload["result"], "Hello World")
        self.assertEqual(payload["shift"], 3)

    def test_preserves_leading_and_trailing_spaces(self):
        payload = web_index.run_cipher("encrypt", "  Hello  ", 3)
        self.assertEqual(payload["text"], "  Hello  ")
        self.assertEqual(payload["result"], "  Khoor  ")

    def test_empty_text_raises_400(self):
        with self.assertRaises(HTTPException) as ctx:
            web_index.run_cipher("encrypt", "   ", 3)
        self.assertEqual(ctx.exception.status_code, 400)

    def test_unknown_mode_raises_400(self):
        with self.assertRaises(HTTPException) as ctx:
            web_index.run_cipher("hack", "Hello", 3)
        self.assertEqual(ctx.exception.status_code, 400)


@unittest.skipUnless(web_index is not None, "FastAPI/Pydantic not installed - skipping web tests")
class TestCipherRequestValidation(unittest.TestCase):
    """Tests for the POST JSON body model (CipherRequest)."""

    def test_boolean_shift_is_rejected(self):
        from pydantic import ValidationError

        with self.assertRaises(ValidationError):
            web_index.CipherRequest(text="Hi", shift=True)

    def test_valid_int_shift_is_accepted(self):
        req = web_index.CipherRequest(text="Hi", shift=3)
        self.assertEqual(req.shift, 3)

    def test_default_shift_is_zero(self):
        req = web_index.CipherRequest(text="Hi")
        self.assertEqual(req.shift, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)