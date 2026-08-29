"""
caesar_cipher.py (web copy)
===========================

This is a frozen copy of the cipher logic used by the CLI version at
the repository root (../caesar_cipher.py). It is duplicated inside
the web/ folder so the Vercel deployment is fully self-contained
(Vercel uploads only the folder being deployed).

If the root cipher ever changes, update this file to match.
Keep its public API identical: encrypt(text, shift), decrypt(text, shift),
normalize_shift(shift).
"""

# The alphabet determines which characters are treated as letters.
ALPHABET_SIZE = 26


def normalize_shift(shift):
    """
    Convert any shift value into the range 0 to 25.

    Because the alphabet only has 26 letters, a shift of 29 behaves
    exactly like a shift of 3 (29 % 26 == 3). The modulo operator
    also handles negative shifts cleanly: -1 becomes 25.

    Parameters
    ----------
    shift : int
        The shift value entered by the user. Can be any integer,
        including numbers larger than 26, or negative numbers.

    Returns
    -------
    int
        The normalized shift value in the range 0 to 25.

    Raises
    ------
    ValueError
        If `shift` is not a whole number (int).
    """
    if isinstance(shift, bool) or not isinstance(shift, int):
        raise ValueError("The shift key must be a whole number (int).")
    return shift % ALPHABET_SIZE


def shift_char(char, shift):
    """
    Shift a single alphabetic character by the given amount.

    Non-alphabetic characters (spaces, digits, punctuation, etc.)
    are returned unchanged.

    Parameters
    ----------
    char : str
        A single character.
    shift : int
        The number of positions to shift (already normalized).

    Returns
    -------
    str
        The shifted character.

    Notes
    -----
    Only the English letters A-Z and a-z are checked explicitly using
    character ranges. `str.isalpha()` is NOT used here because it also
    returns True for non-English letters (e, n, ss, Cyrillic, ...),
    which would get scrambled instead of preserved.
    """
    # Only shift the 26 English letters, in both cases.
    if ("a" <= char <= "z") or ("A" <= char <= "Z"):
        # 'A' has code 65 and 'a' has code 97. We work with the
        # position of the letter inside the alphabet (0 to 25).
        base = ord("A") if char.isupper() else ord("a")
        position = ord(char) - base
        new_position = (position + shift) % ALPHABET_SIZE
        return chr(base + new_position)
    # Everything else (spaces, digits, punctuation, non-English
    # letters, emoji, ...) passes through untouched.
    return char


def encrypt(text, shift):
    """
    Encrypt text using the Caesar Cipher.

    Each letter is shifted *forward* by the shift amount.
    Uppercase and lowercase letters are both supported.

    Parameters
    ----------
    text : str
        The plain text to encrypt.
    shift : int
        The shift key. Can be any integer; it is normalized
        automatically to the range 0 to 25.

    Returns
    -------
    str
        The encrypted text.

    Raises
    ------
    ValueError
        If `shift` is not a whole number (int).
    """
    shift = normalize_shift(shift)
    return "".join(shift_char(char, shift) for char in text)


def decrypt(text, shift):
    """
    Decrypt text that was encrypted with the Caesar Cipher.

    Each letter is shifted *backward* by the shift amount, which
    undoes the encryption. Decrypting a text with shift N is the
    same as encrypting it with shift -N.

    Parameters
    ----------
    text : str
        The cipher text to decrypt.
    shift : int
        The shift key that was originally used for encryption.

    Returns
    -------
    str
        The decrypted (original) text.

    Raises
    ------
    ValueError
        If `shift` is not a whole number (int).
    """
    # Validate and normalize FIRST so the negation below never sees
    # an invalid type (e.g. None or "3"), which would raise a raw
    # TypeError instead of the friendly ValueError.
    shift = normalize_shift(shift)
    return encrypt(text, -shift)