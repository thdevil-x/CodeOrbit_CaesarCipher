"""
main.py
=======

CaesarCrypt - Caesar Cipher Encryption Tool
===========================================

This is the interactive command-line interface (CLI) for the project.

The program:
    1. Shows an explanation of the Caesar Cipher.
    2. Lets the user encrypt or decrypt text with any shift key.
    3. Runs in a loop so the user can do many operations without
       restarting.
    4. Validates all input and shows friendly error messages.
"""

from caesar_cipher import encrypt, decrypt, normalize_shift


# Display constants (dividers used to make the output look tidy).
LINE = "=" * 40
SUB_LINE = "-" * 40


def show_banner():
    """Display the professional project banner and title."""
    print()
    print(LINE)
    print("       CaesarCrypt")
    print("   Caesar Cipher Encryption Tool")
    print(LINE)


def show_explanation():
    """
    Print a short, beginner-friendly explanation of how
    the Caesar Cipher works.
    """
    print()
    print("HOW IT WORKS")
    print(SUB_LINE)
    print("Caesar Cipher is a classical substitution cipher that")
    print("shifts alphabetic characters by a selected number of")
    print("positions, called the shift key.")
    print()
    print('Example with key 3:  "A" becomes "D", "B" becomes "E",')
    print('"Z" wraps around and becomes "C".')
    print()
    print("Only letters are changed. Spaces, numbers and special")
    print("characters stay the same. This is an educational tool,")
    print("so it is NOT secure for real confidential information.")
    print(SUB_LINE)


def show_menu():
    """Print the main menu options."""
    print()
    print("1. Encrypt Text")
    print("2. Decrypt Text")
    print("3. Exit")
    print()


def get_int(prompt):
    """
    Ask the user for a whole number and keep asking until they
    enter something valid.

    Parameters
    ----------
    prompt : str
        The text shown to the user.

    Returns
    -------
    int
        A valid integer entered by the user.
    """
    while True:
        user_input = input(prompt).strip()
        try:
            return int(user_input)
        except ValueError:
            print("Invalid input! Please enter a whole number (integer).")
            print()


def get_text(prompt):
    """
    Ask the user for some text and make sure it is not empty.

    The text is returned exactly as typed. Leading and trailing
    spaces are preserved, because the cipher should keep spaces
    untouched.

    Parameters
    ----------
    prompt : str
        The text shown to the user.

    Returns
    -------
    str
        The text entered by the user (not stripped).
    """
    while True:
        user_input = input(prompt)
        # Check for "empty" (only whitespace) but keep the original.
        if user_input.strip():
            return user_input
        print("Text cannot be empty. Please enter some text.")
        print()


def choose_shift():
    """
    Ask the user for a shift key (any integer, possibly large or
    negative). Returns the raw value; it gets normalized later, both
    by the cipher and for display.
    """
    return get_int("Enter shift key: ")


def show_results(mode, text, result, shift):
    """
    Print the results of an operation in a clear, readable format.

    The effective (normalized) shift is shown, and if the user typed
    a shift outside the range 0-25, a note explains how it was
    normalized.

    Parameters
    ----------
    mode : str
        Either "encrypt" or "decrypt". Decides how the input row is
        labelled ("Original Text" vs "Encrypted Text").
    text : str
        The text the user provided.
    result : str
        The transformed output.
    shift : int
        The shift key that was used (raw value from the user).
    """
    effective_shift = normalize_shift(shift)

    # Labels adapt to the operation being shown.
    if mode == "encrypt":
        label_input = "Original Text"
        label_output = "Encrypted Text"
    else:
        label_input = "Encrypted Text"
        label_output = "Decrypted Text"

    print()
    print(SUB_LINE)
    print(f"{label_input:<15}: {text}")
    print(f"{label_output:<15}: {result}")
    print(f"{'Shift Key':<15}: {effective_shift}")
    if effective_shift != shift:
        print(f"{'Note':<15}: {shift} normalized to {effective_shift}.")
    print(SUB_LINE)


def show_exit_message():
    """
    Print the closing message before the program terminates.

    The lock emoji is shown when the terminal can print it; a plain
    version is used as a fallback for older consoles so the program
    never crashes just because of a missing Unicode character.
    """
    print()
    print(LINE)
    print("Thank you for using CaesarCrypt!")
    try:
        print("Stay Secure. 🔐")
    except UnicodeEncodeError:
        print("Stay Secure.")
    print(LINE)


def run():
    """Run the main interactive loop of the program."""
    show_banner()
    show_explanation()

    try:
        while True:
            show_menu()

            # Get a valid menu choice (1, 2 or 3).
            choice = get_int("Enter your choice: ")

            if choice == 1:
                # ---- ENCRYPT ----
                print()
                text = get_text("Enter text: ")
                shift = choose_shift()
                encrypted = encrypt(text, shift)
                show_results("encrypt", text, encrypted, shift)

            elif choice == 2:
                # ---- DECRYPT ----
                print()
                text = get_text("Enter encrypted text: ")
                shift = choose_shift()
                decrypted = decrypt(text, shift)
                show_results("decrypt", text, decrypted, shift)

            elif choice == 3:
                # ---- EXIT ----
                break

            else:
                print(f"Invalid choice '{choice}'. Please choose 1, 2 or 3.")
                print()

    except KeyboardInterrupt:
        # User pressed Ctrl+C - stop quietly instead of crashing.
        print()
        print("Interrupted by user (Ctrl+C).")
    except EOFError:
        # No more input (Ctrl+D or redirected file ended) - stop neatly.
        print()
        print("End of input reached.")
    finally:
        # Always say goodbye, no matter how we left the loop.
        show_exit_message()


# Only start the program when this file is run directly
# (not when it is imported by another file).
if __name__ == "__main__":
    run()