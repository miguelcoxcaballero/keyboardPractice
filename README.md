# keyboardPractice

This project is a typing practice application in Python designed to help improve typing speed and accuracy. The application includes three modes: single characters, random words, and C++ phrases. It uses PyQt5 for a graphical interface, providing an intuitive user experience.

## Mode Descriptions

1. **Mode 1 - Single Characters**: This mode generates random individual characters, including letters, symbols, and special characters. It is ideal for practicing accuracy with single key presses.

2. **Mode 2 - Random Words**: In this mode, the program displays random words from a text file (`palabras.txt`). This mode helps to improve typing speed for complete words.

3. **Mode 3 - C++ Phrases**: This mode presents C++-related phrases from the file `frases.txt`. It allows you to practice typing full sentences, especially useful for improving fluency in typing technical text.

## Customizing Content

To customize the practice content:
- **palabras.txt**: Add words, one per line, for Mode 2.
- **frases.txt**: Add phrases, one per line, for Mode 3, preferably programming or C++ phrases.

## Removing Unwanted Characters

If your keyboard lacks certain characters, such as the Spanish "ñ" or accented letters, you can remove them from the `char_list` in the code to prevent them from appearing in Mode 1.

To do so:
1. Open `main.py`.
2. Find the variable `char_list` and remove the unwanted characters, such as `'ñ'`, `'á'`, `'é'`, etc.
3. Save the file and run the program again.

## Package Installation

Ensure you have Python 3.x and the following packages installed:

```bash
pip install PyQt5
