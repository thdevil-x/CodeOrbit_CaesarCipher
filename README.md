# CaesarCrypt – Caesar Cipher Encryption Tool

> A beginner-friendly Python cybersecurity project that encrypts and
> decrypts text using the **Caesar Cipher**, one of the oldest and most
> famous encryption techniques in history.

---

## 1. Project Overview

CaesarCrypt is a command-line (CLI) program written in Python 3. It lets
you encrypt a message by shifting each letter forward in the alphabet by a
number of your choice (the **shift key**), and decrypt it back by shifting
letters the opposite way.

- **Encrypt:** `Hello World` → `Khoor Zruog` (key = 3)
- **Decrypt:** `Khoor Zruog` → `Hello World` (key = 3)

The program is **interactive**: you pick an action from a menu, type your
text, type a shift key, and read the result. You can keep encrypting and
decrypting without ever restarting the program.

---

## 2. Project Objective

The goal of this project is to demonstrate:

1. How classical encryption works in practice.
2. How to build a clean, testable Python CLI application.
3. How to validate user input and handle errors gracefully.
4. How modulo arithmetic makes alphabet "wrap-around" easy.
5. How to structure a small, reusable Python package (logic + CLI + tests)
   that is ready to share on GitHub.

---

## 3. Features

- Interactive, menu-driven command-line interface.
- Encrypt and decrypt any text with a user-chosen shift key.
- Supports **uppercase** letters (`A-Z`) and **lowercase** letters (`a-z`).
- Preserves **spaces, numbers and special characters** (e.g. `!`, `?`, `@`, `1`, `.`).
- Preserves non-English letters (`é`, `ñ`, `ß`, Cyrillic, emoji, ...) untouched.
- Preserves leading/trailing spaces exactly as typed.
- Handles **shift values greater than 26** by normalizing with modulo 26
  (e.g. `29 → 3`).
- Handles **negative shift** values correctly (e.g. `-3 → 23`).
- Full **input validation** with friendly error messages – never crashes.
- Loop-based menu: perform many encrypt/decrypt operations in one session.
- Built-in explanation of how the Caesar Cipher works.
- Professional exit message.
- Unit tests using Python's built-in `unittest` module.
- **Zero external dependencies** – only the Python standard library.

---

## 4. Technologies Used

| Technology        | Usage                              |
|-------------------|------------------------------------|
| Python 3.6+       | Programming language               |
| `unittest`        | Built-in testing framework         |
| Standard library  | No third-party packages required   |

**No external libraries are used or required.**

---

## 5. How the Caesar Cipher Works

The Caesar Cipher is a **substitution cipher** named after Julius Caesar,
who used it for private correspondence around 58 BC.

Every letter in your message is replaced by the letter found a fixed number
of positions further down the alphabet. That fixed number is the **shift key**.

Because the alphabet has only **26 letters**, the cipher uses
**modulo arithmetic** (`% 26`) to wrap around:

> After `Z` comes `A` again. After `z` comes `a` again.

### Encryption formula

```text
new_position = (old_position + shift) % 26
```

### Decryption formula

```text
new_position = (old_position - shift) % 26
```

### Shift table (key = 3)

| Plain | Cipher |
|-------|--------|
| A     | D      |
| B     | E      |
| C     | F      |
| X     | A      |
| Y     | B      |
| Z     | C      |

---

## 6. Encryption Logic

Encryption **shifts each letter forward** by the key:

```text
A → D    (shift +3)
B → E    (shift +3)
X → A    (shift +3, wraps around)
Z → C    (shift +3, wraps around)
```

Only the 26 English letters are shifted. Each letter keeps its case:
`Hello` encrypts to `Khoor`, not `KHOOR` or `khoor`.

Numbers, spaces, punctuation and special characters are **left unchanged**.

---

## 7. Decryption Logic

Decryption is the exact reverse: it **shifts each letter backward** by the same key.

Math note: decrypting with key `N` is identical to encrypting with key `-N`.

Encryption and decryption are **perfectly symmetric**, so:

```text
decrypt(encrypt(text, shift), shift) == text
```

---

## 8. Example

```text
Plaintext:  Hello World
Shift:      3

Encrypted:  Khoor Zruog
Decrypted:  Hello World
```

Step by step for `H` with key `3`:

| Step                          | Result |
|-------------------------------|--------|
| Encryption:  H + 3            | K      |
| Decryption:  K - 3            | H      |
| Wrap-around: Z + 1            | A      |
| Wrap-around: A - 1            | Z      |

---

## 9. Project Structure

```text
CaesarCrypt/
│
├── main.py                     # Interactive CLI (menu, input, output)
├── caesar_cipher.py            # Core cipher logic (encrypt / decrypt)
├── requirements.txt            # No external dependencies
├── README.md                   # This file
├── .gitignore                  # Git exclusions for Python projects
│
├── tests/
│   ├── __init__.py             # Makes tests a Python package
│   └── test_caesar_cipher.py   # Unit tests for the cipher logic
│
└── web/                        # Optional: FastAPI web version (Vercel-ready)
    ├── api/index.py            # FastAPI app (HTML form + JSON API)
    ├── caesar_cipher.py        # Cipher logic copy (self-contained deploy)
    ├── requirements.txt        # fastapi, uvicorn, python-multipart
    ├── vercel.json             # Vercel Python runtime config
    └── README.md               # Web version docs + deploy instructions
```

The **web version is optional**. The main project is the CLI tool above;
`web/` is a separate, self-contained deployable web app so you can test
deploying it on Vercel (see `web/README.md`).

---

## 10. Installation

### Prerequisites

- **Python 3.6 or newer** installed on your machine.
  Check with: `python --version` (or `python3 --version`).
- No external packages are needed.

### Steps

1. Open a terminal and go to the project folder:

   ```bash
   cd CaesarCrypt
   ```

2. (Optional but recommended) Create a virtual environment:

   ```bash
   python -m venv venv
   ```

   Activate it:

   - **Windows (Command Prompt):** `venv\Scripts\activate`
   - **Windows (PowerShell):** `venv\Scripts\Activate.ps1`
   - **Linux / macOS:** `source venv/bin/activate`

3. There is nothing else to install — the project uses only the standard
   library. `pip install -r requirements.txt` would simply do nothing.

---

## 11. Running the Project

Run this command from the project folder:

```bash
python main.py
```

Or on systems where Python is installed as `python3`:

```bash
python3 main.py
```

### Example commands by platform

| Platform            | Command               |
|---------------------|-----------------------|
| Windows (CMD/PowerShell) | `python main.py`  |
| VS Code terminal    | `python main.py`  |
| Linux               | `python3 main.py` |
| macOS               | `python3 main.py` |

> In VS Code: open the `CaesarCrypt` folder, open the integrated terminal
> with `` Ctrl+` ``, and run the command above.

---

## 12. Testing

The project ships with a full unit-test suite.

### Run all tests

From the project root folder:

```bash
python -m unittest discover -s tests -v
```

Or:

```bash
python -m unittest tests.test_caesar_cipher -v
```

Expected output ends with:

```text
Ran 27 tests in 0.00Xs

OK
```

(The exact runtime varies by machine; a green `OK` with **27 passed, 0 failed** is what matters.)

### What is tested

- Uppercase encryption (`ABC` → `DEF`)
- Uppercase wrap-around (`XYZ` → `ABC`)
- Lowercase encryption (`abc` → `def`)
- Lowercase wrap-around (`xyz` → `abc`)
- Mixed case
- Spaces preserved
- Numbers preserved (`Hello123!` → `Khoor123!`)
- Special characters preserved
- Shift `0` (text unchanged)
- Shift `26` (same as `0`)
- Shift greater than 26 (`29` works like `3`)
- Large positive shifts (`1000`)
- Negative shifts (`-3`)
- Very large negative shifts (`-26`)
- Empty text
- Decryption of all the above
- Shift normalization (`29→3`, `26→0`, `52→0`, `-3→23`)
- Rejecting non-integer shift keys (`2.5`, `"3"`, `None`, `True`)
- Round-trip: `decrypt(encrypt(text, shift), shift) == text`

---

## 13. Sample Terminal Output

```text
========================================
       CaesarCrypt
   Caesar Cipher Encryption Tool
========================================

HOW IT WORKS
----------------------------------------
Caesar Cipher is a classical substitution cipher that
shifts alphabetic characters by a selected number of
positions, called the shift key.

Example with key 3:  "A" becomes "D", "B" becomes "E",
"Z" wraps around and becomes "C".

Only letters are changed. Spaces, numbers and special
characters stay the same. This is an educational tool,
so it is NOT secure for real confidential information.
----------------------------------------

1. Encrypt Text
2. Decrypt Text
3. Exit

Enter your choice: 1

Enter text: Hello World
Enter shift key: 3

----------------------------------------
Original Text  : Hello World
Encrypted Text : Khoor Zruog
Shift Key      : 3
----------------------------------------

1. Encrypt Text
2. Decrypt Text
3. Exit

Enter your choice: 2

Enter encrypted text: Khoor Zruog
Enter shift key: 3

----------------------------------------
Encrypted Text : Khoor Zruog
Decrypted Text : Hello World
Shift Key      : 3
----------------------------------------

1. Encrypt Text
2. Decrypt Text
3. Exit

Enter your choice: 3

========================================
Thank you for using CaesarCrypt!
Stay Secure. 🔐
========================================
```

---

## 14. Input Validation

The program never crashes on bad input. Every user input is validated:

| Situation                | Program response                                        |
|--------------------------|---------------------------------------------------------|
| Invalid menu choice      | `Invalid choice '7'. Please choose 1, 2 or 3.`          |
| Non-integer menu choice  | `Invalid input! Please enter a whole number (integer).` |
| Non-integer shift key    | `Invalid input! Please enter a whole number (integer).` |
| Empty text               | `Text cannot be empty. Please enter some text.`         |
| Very large shift (e.g. 1000000) | Normalized automatically with `% 26`.           |
| Negative shift (e.g. -3) | Normalized automatically (`-3 → 23`).                  |
| `Ctrl+C` / `Ctrl+D` when typing | Clean exit message instead of a crash.          |

A friendly note explains when a shift is normalized outside 0–25:

```text
Note           : 29 normalized to 3.
```

---

## 15. Limitations of the Caesar Cipher

- **Only 26 possible keys** – a brute-force attack tries every key in seconds.
- **Vulnerable to frequency analysis** – common letters like `E` stay common
  in the cipher text, leaking information about the plaintext.
- **No key security** – once someone knows the key, the message is open.
- **Only letters are hidden** – spaces, numbers and punctuation are exposed,
  which reveals word lengths and structure.
- **Entirely breakable by computer** – it offers real security to nobody.

---

## 16. Security Disclaimer

> **IMPORTANT:** The Caesar Cipher is a **classical educational cipher**.
> It is **NOT secure** for protecting real-world confidential information
> such as passwords, credit card numbers, or private messages.

Modern systems use **strong cryptographic algorithms** (e.g. AES, RSA,
Argon2, TLS) that are mathematically designed to resist attacks.
CaesarCrypt exists purely for **learning and demonstration purposes** —
never rely on it to secure real data.

---

## 17. Educational Purpose

This project teaches the foundations of cryptography:

- What a **cipher** and a **key** are.
- How **substitution ciphers** work.
- Why **modulo arithmetic** keeps letters in the alphabet.
- Why encryption **must be reversible** (encrypt ↔ decrypt).
- Why brute force is easy when the key space is tiny.


---

## 18. Learning Outcomes

After exploring this project you will be able to:

1. Explain how the Caesar Cipher encrypts and decrypts text.
2. Use modulo (`%`) to wrap alphabet indices around after `Z`/`z`.
3. Write reusable Python functions with docstrings (`encrypt`, `decrypt`).
4. Build an interactive CLI with a menu loop.
5. Validate user input and handle errors with `try/except`.
6. Write and run unit tests with Python's built-in `unittest`.
7. Structure a small project for GitHub (`main`, module, tests, README, .gitignore`).
8. Talk about the security limits of classical ciphers.

---

## 19. Future Improvements

1. **Automatic brute-force decoder** – try all 26 shifts and score the
   results against English letter frequencies to crack any Caesar message.
2. **Vigenère Cipher** – a polyalphabetic cipher that uses a keyword and is
   far stronger than Caesar (still easy to learn and implement).
3. **File encryption** – read text from a `.txt` file, encrypt it, and save
   the output to a new file.
4. **Fancy terminal output** – colored text, progress animation and a nicer
   box-drawing UI using ANSI escape codes.
5. **GUI version** – a small Tkinter window with an input box, a shift
   slider, and live encrypt/decrypt preview as you type.

---

## 20. Author

**Project:** CaesarCrypt – Caesar Cipher Encryption Tool
**Created by:** CodeOrbit Tech Intern – Cybersecurity Track
**Repository:** `CodeOrbit_CaesarCipher`
**Language:** Python 3 · **License:** Free for educational use

---

Made with Python and a love for the classics. 🔐