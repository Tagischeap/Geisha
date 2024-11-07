# core/seasonal_handler.py
import datetime
import os

SEASONAL_WORDS_PATH = os.path.join("features", "seasonal")

def get_current_season():
    """Determine the current holiday season based on the date."""
    today = datetime.date.today()
    month, day = today.month, today.day

    if (month == 10) or (month == 11 and day == 1):  # Halloween: October and November 1st
        return "halloween"
    elif (month == 11 and day >= 15) or (month == 12) or (month == 1 and day == 1):  # Christmas: Mid-November to New Year's Day
        return "christmas"
    else:
        return None  # No active season

def load_word_bank_and_emojis(season):
    """Load word bank and emojis for the specified season."""
    words = set()
    emojis = []

    # Load words for the season
    word_file = os.path.join(SEASONAL_WORDS_PATH, f"{season}_words.txt")
    if os.path.isfile(word_file):
        with open(word_file, "r", encoding="utf-8-sig") as file:
            words = set(line.strip().lower() for line in file if line.strip())

    # Load emojis for the season
    emoji_file = os.path.join(SEASONAL_WORDS_PATH, f"{season}_emojis.txt")
    if os.path.isfile(emoji_file):
        with open(emoji_file, "r", encoding="utf-8-sig") as file:
            emojis = [line.strip() for line in file if line.strip()]

    return words, emojis
