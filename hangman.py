"""
Advanced Hangman Game - CodeAlpha Internship Task 1
Features: OOP, difficulty levels, categories, hints, stats tracking
"""

import random
import json
import os
from datetime import datetime

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    # Fallback if colorama not installed
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Style:
        BRIGHT = RESET_ALL = ""


class HangmanGame:
    """Object-Oriented Hangman Game"""
    
    # Word database with categories and difficulty
    WORD_DATABASE = {
        "animals": {
            "easy": ["cat", "dog", "lion", "bear", "fish"],
            "medium": ["elephant", "giraffe", "dolphin", "penguin", "kangaroo"],
            "hard": ["chimpanzee", "rhinoceros", "hippopotamus", "orangutan", "platypus"]
        },
        "technology": {
            "easy": ["code", "data", "web", "app", "bot"],
            "medium": ["python", "server", "cloud", "router", "kernel"],
            "hard": ["algorithm", "microservice", "virtualization", "cryptography", "blockchain"]
        },
        "countries": {
            "easy": ["india", "china", "japan", "egypt", "peru"],
            "medium": ["australia", "argentina", "germany", "brazil", "canada"],
            "hard": ["uzbekistan", "liechtenstein", "mozambique", "kyrgyzstan", "turkmenistan"]
        }
    }
    
    # ASCII art for hangman
    HANGMAN_STAGES = [
        """
          +---+
              |
              |
              |
             ===""",
        """
          +---+
          O   |
              |
              |
             ===""",
        """
          +---+
          O   |
          |   |
              |
             ===""",
        """
          +---+
          O   |
         /|   |
              |
             ===""",
        """
          +---+
          O   |
         /|\\  |
              |
             ===""",
        """
          +---+
          O   |
         /|\\  |
         /    |
             ===""",
        """
          +---+
          O   |
         /|\\  |
         / \\  |
             ==="""
    ]
    
    def __init__(self):
        self.max_wrong = 6
        self.stats_file = "stats.json"
        self.stats = self._load_stats()
        self.current_word = ""
        self.guessed_letters = []
        self.wrong_guesses = 0
        self.hints_used = 0
        self.max_hints = 2
        self.category = ""
        self.difficulty = ""
    
    def _load_stats(self):
        """Load player statistics"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, "r") as f:
                    return json.load(f)
            except:
                pass
        return {
            "games_played": 0,
            "games_won": 0,
            "games_lost": 0,
            "current_streak": 0,
            "best_streak": 0,
            "total_hints_used": 0,
            "last_played": None
        }
    
    def _save_stats(self):
        """Save player statistics"""
        with open(self.stats_file, "w") as f:
            json.dump(self.stats, f, indent=4)
    
    def _display_banner(self):
        """Display game banner"""
        banner = f"""
{Fore.CYAN}{Style.BRIGHT}
╔═══════════════════════════════════════════╗
║         🎮  HANGMAN GAME  🎮              ║
║      Advanced Edition - CodeAlpha         ║
╚═══════════════════════════════════════════╝
{Style.RESET_ALL}"""
        print(banner)
    
    def _select_difficulty(self):
        """Select difficulty level"""
        print(f"\n{Fore.YELLOW}📊 Select Difficulty Level:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}1. Easy{Style.RESET_ALL}    (5-6 letter words)")
        print(f"  {Fore.YELLOW}2. Medium{Style.RESET_ALL}  (7-9 letter words)")
        print(f"  {Fore.RED}3. Hard{Style.RESET_ALL}    (10+ letter words)")
        
        while True:
            choice = input(f"\n{Fore.CYAN}Enter choice (1-3): {Style.RESET_ALL}").strip()
            if choice in ["1", "2", "3"]:
                return {"1": "easy", "2": "medium", "3": "hard"}[choice]
            print(f"{Fore.RED}⚠️ Invalid choice. Please enter 1, 2, or 3.{Style.RESET_ALL}")
    
    def _select_category(self):
        """Select word category"""
        categories = list(self.WORD_DATABASE.keys())
        print(f"\n{Fore.YELLOW}📚 Select Word Category:{Style.RESET_ALL}")
        for i, cat in enumerate(categories, 1):
            print(f"  {Fore.GREEN}{i}. {cat.title()}{Style.RESET_ALL}")
        
        while True:
            choice = input(f"\n{Fore.CYAN}Enter choice (1-{len(categories)}): {Style.RESET_ALL}").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(categories):
                return categories[int(choice) - 1]
            print(f"{Fore.RED}⚠️ Invalid choice.{Style.RESET_ALL}")
    
    def _setup_new_round(self):
        """Setup new game round"""
        self.difficulty = self._select_difficulty()
        self.category = self._select_category()
        
        word_list = self.WORD_DATABASE[self.category][self.difficulty]
        self.current_word = random.choice(word_list).lower()
        self.guessed_letters = []
        self.wrong_guesses = 0
        self.hints_used = 0
        
        print(f"\n{Fore.GREEN}✅ New game started!{Style.RESET_ALL}")
        print(f"   Category: {Fore.CYAN}{self.category.title()}{Style.RESET_ALL}")
        print(f"   Difficulty: {Fore.CYAN}{self.difficulty.title()}{Style.RESET_ALL}")
        print(f"   Word length: {Fore.YELLOW}{len(self.current_word)} letters{Style.RESET_ALL}\n")
    
    def _get_display_word(self):
        """Get current word display"""
        return " ".join([
            Fore.GREEN + letter + Style.RESET_ALL 
            if letter in self.guessed_letters 
            else Fore.WHITE + "_" + Style.RESET_ALL 
            for letter in self.current_word
        ])
    
    def _display_hangman(self):
        """Display hangman ASCII art"""
        stage = self.HANGMAN_STAGES[self.wrong_guesses]
        color = Fore.GREEN if self.wrong_guesses < 3 else (Fore.YELLOW if self.wrong_guesses < 5 else Fore.RED)
        print(f"\n{color}{stage}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Wrong guesses: {self.wrong_guesses}/{self.max_wrong}{Style.RESET_ALL}\n")
    
    def _display_game_state(self):
        """Display complete game state"""
        os.system("cls" if os.name == "nt" else "clear")
        self._display_banner()
        self._display_hangman()
        print(f"{Fore.CYAN}{Style.BRIGHT}Word: {self._get_display_word()}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Guessed Letters: {', '.join(sorted(self.guessed_letters)) or 'None'}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Hints Remaining: {self.max_hints - self.hints_used}{Style.RESET_ALL}\n")
    
    def _use_hint(self):
        """Provide a hint"""
        if self.hints_used >= self.max_hints:
            return "❌ No hints remaining!"
        
        unguessed = [l for l in self.current_word if l not in self.guessed_letters]
        if not unguessed:
            return "❌ No hints available!"
        
        hint_letter = random.choice(unguessed)
        self.hints_used += 1
        self.stats["total_hints_used"] += 1
        return f"💡 Hint: The letter '{Fore.GREEN}{hint_letter.upper()}{Style.RESET_ALL}' is in the word!"
    
    def _handle_guess(self, guess):
        """Process player's guess"""
        if guess == "?":
            return True, self._use_hint()
        
        if len(guess) != 1 or not guess.isalpha():
            return False, f"{Fore.RED}⚠️ Please enter a single valid letter.{Style.RESET_ALL}"
        
        if guess in self.guessed_letters:
            return False, f"{Fore.YELLOW}⚠️ You already guessed '{guess.upper()}'!{Style.RESET_ALL}"
        
        self.guessed_letters.append(guess)
        
        if guess in self.current_word:
            return False, f"{Fore.GREEN}✅ Good! '{guess.upper()}' is in the word.{Style.RESET_ALL}"
        else:
            self.wrong_guesses += 1
            return False, f"{Fore.RED}❌ Sorry, '{guess.upper()}' is NOT in the word.{Style.RESET_ALL}"
    
    def _check_game_status(self):
        """Check game status"""
        if all(letter in self.guessed_letters for letter in self.current_word):
            return "won"
        if self.wrong_guesses >= self.max_wrong:
            return "lost"
        return "ongoing"
    
    def _update_stats(self, result):
        """Update statistics"""
        self.stats["games_played"] += 1
        self.stats["last_played"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if result == "won":
            self.stats["games_won"] += 1
            self.stats["current_streak"] += 1
            self.stats["best_streak"] = max(self.stats["best_streak"], self.stats["current_streak"])
        else:
            self.stats["games_lost"] += 1
            self.stats["current_streak"] = 0
        
        self._save_stats()
    
    def _display_stats(self):
        """Display statistics"""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}📊 YOUR STATISTICS:{Style.RESET_ALL}")
        print(f"{'─' * 40}")
        print(f"  Games Played:    {Fore.WHITE}{self.stats['games_played']}{Style.RESET_ALL}")
        print(f"  Games Won:       {Fore.GREEN}{self.stats['games_won']}{Style.RESET_ALL}")
        print(f"  Games Lost:      {Fore.RED}{self.stats['games_lost']}{Style.RESET_ALL}")
        win_rate = (self.stats['games_won'] / self.stats['games_played'] * 100) if self.stats['games_played'] > 0 else 0
        print(f"  Win Rate:        {Fore.YELLOW}{win_rate:.1f}%{Style.RESET_ALL}")
        print(f"  Current Streak:  {Fore.MAGENTA}{self.stats['current_streak']} 🔥{Style.RESET_ALL}")
        print(f"  Best Streak:     {Fore.CYAN}{self.stats['best_streak']} 🏆{Style.RESET_ALL}")
        print(f"{'─' * 40}\n")
    
    def play(self):
        """Main game loop"""
        self._display_banner()
        
        while True:
            self._setup_new_round()
            
            while True:
                self._display_game_state()
                guess = input(f"{Fore.CYAN}Guess a letter (or '?' for hint): {Style.RESET_ALL}").lower().strip()
                
                is_hint, message = self._handle_guess(guess)
                print(message)
                
                if not is_hint:
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                
                status = self._check_game_status()
                if status != "ongoing":
                    break
            
            # Game over
            self._display_game_state()
            self._update_stats(status)
            
            if status == "won":
                print(f"\n{Fore.GREEN}{Style.BRIGHT}🎉 CONGRATULATIONS! You guessed '{self.current_word.upper()}'!{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}{Style.BRIGHT}💀 GAME OVER! The word was: '{self.current_word.upper()}'{Style.RESET_ALL}")
            
            self._display_stats()
            
            replay = input(f"\n{Fore.CYAN}Play again? (y/n): {Style.RESET_ALL}").lower().strip()
            if replay != "y":
                print(f"\n{Fore.MAGENTA}👋 Thanks for playing! See you soon!{Style.RESET_ALL}\n")
                break


if __name__ == "__main__":
    try:
        game = HangmanGame()
        game.play()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}⚠️ Game interrupted. Goodbye!{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"\n{Fore.RED}❌ An error occurred: {e}{Style.RESET_ALL}\n")