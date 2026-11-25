# Hangman Game — Advanced Edition 🎮

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)

**CodeAlpha Internship — Task 1**

A feature-rich, object-oriented Hangman game for the terminal. Pick a category and difficulty, guess letters, use hints wisely, and track your win streak across sessions.

> 📝 **Note on the repo name:** the repository is named `CodeAlpha_HungmanGame` (a typo from the original upload). The game itself is Hangman — the repo name is kept as-is to avoid breaking existing links.

## ✨ Features

- 🧱 **Object-oriented design** — a clean `HangmanGame` class with separate methods for setup, gameplay, and stats
- 📚 **3 word categories** — Animals, Technology, Countries
- 📊 **3 difficulty levels** — Easy (5–6 letters), Medium (7–9), Hard (10+)
- 💡 **Hint system** — up to 2 hints per game (reveals a letter)
- 📈 **Persistent stats** — games played/won/lost, current & best streaks, hints used, saved to `stats.json`
- 🎨 **Colored terminal output** — via `colorama` (gracefully falls back to plain text if not installed)
- 🪢 **ASCII hangman art** — 7 progressive stages as wrong guesses add up

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.8+ (standard library only, plus optional `colorama`) |
| Data | In-code word database (45 words across 3 categories × 3 difficulties) |
| Persistence | `stats.json` (created automatically on first run) |

## 🚀 Run

**Prerequisites:** Python 3.8+.

```bash
# Clone the repo
git clone https://github.com/hamidraza-bot/CodeAlpha_HungmanGame.git
cd CodeAlpha_HungmanGame

# (Optional) colored output
pip install -r requirements.txt

# Play
python hangman.py
```

No installation is strictly required — the game runs with the standard library alone and falls back to plain text if `colorama` is missing.

## 🎮 How to Play

1. Choose a **difficulty** (Easy / Medium / Hard).
2. Choose a **category** (Animals / Technology / Countries).
3. Guess one letter at a time — you get **6 wrong guesses** before the hangman is complete.
4. Type `hint` (up to 2 per game) to reveal a letter, or guess the full word if you're confident.
5. Your stats are saved to `stats.json` and shown after each game.

## 📁 Project Structure

```
├── hangman.py          # The game — OOP design, word database, stats tracking
├── requirements.txt    # Optional: colorama (for colored terminal output)
├── .gitignore
├── README.md
└── LICENSE
```

## 📄 License

MIT — see [LICENSE](LICENSE).

---

Built by [Hamid Raza](https://github.com/hamidraza-bot) · AI Automation Engineer · [Fiverr](https://www.fiverr.com/hamid_buildai)
