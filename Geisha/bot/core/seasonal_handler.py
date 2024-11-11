# bot/core/seasonal_handler.py
import datetime
import os

SEASONAL_WORDS_PATH = os.path.join("features", "seasonal")
ICONS_PATH = os.path.join("features", "seasonal")

def get_current_season():
    """Determine the current holiday season based on the date and return the appropriate icon."""
    today = datetime.date.today()

    # Helper function to calculate start and end date for a holiday
    def holiday_range(start_month, start_day, end_month=None, end_day=None):
        start_date = datetime.date(today.year, start_month, start_day) - datetime.timedelta(days=7)
        if end_month and end_day:
            end_date = datetime.date(today.year, end_month, end_day) + datetime.timedelta(days=1)
        else:
            end_date = datetime.date(today.year, start_month, start_day) + datetime.timedelta(days=1)
        return start_date <= today <= end_date

    # Halloween: October 1st to November 1st
    if holiday_range(10, 1, 11, 1):
        return "halloween", os.path.join(ICONS_PATH, "halloween_icon.gif")

    # Christmas: November 15th to January 1st
    elif holiday_range(11, 15, 1, 1):
        return "christmas", os.path.join(ICONS_PATH, "christmas_icon.gif")

    # Valentine's Day: February 14th, with range
    elif holiday_range(2, 14):
        return "valentines", os.path.join(ICONS_PATH, "valentines_icon.gif")

    # Saint Patrick's Day: March 17th, with range
    elif holiday_range(3, 17):
        return "saint_patricks", os.path.join(ICONS_PATH, "saint_patricks_icon.gif")

    # April Fool's Day: Only on April 1
    elif today.month == 4 and today.day == 1:
        return "april_fools", os.path.join(ICONS_PATH, "april_fools_icon.gif")

    # Easter (fixed date example; adjust yearly if needed): April 9th, with range
    elif holiday_range(4, 9):
        return "easter", os.path.join(ICONS_PATH, "easter_icon.gif")

    # Default (no active season)
    return "normal", os.path.join(ICONS_PATH, "normal_icon.gif")

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
