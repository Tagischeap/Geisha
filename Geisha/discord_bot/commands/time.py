import datetime
import pytz
import discord

name = 'time'
aliases = ['t']
description = """
Displays the current time, converts to a specific timezone, or formats a custom time using Discord's timestamp.
Usage: !time [YYYY-MM-DDTHH:MM] [timezone] [format].
Formats: 
- R: Relative time (e.g., "in 5 minutes").
- f: Full date & time (e.g., "December 25, 2024 3:00 PM").
- d: Short date.
- t: Short time.
- T: Long time.
- D: Long date.
- F: Full date & time with weekday.
"""
usage = '[YYYY-MM-DDTHH:MM] [timezone] [format]'
cooldown = 3

async def execute(client, message, args):
    try:
        now = datetime.datetime.now(pytz.utc)
        timezone = "UTC"
        format_code = "f"  # Default to full date and time format
        
        # Check for format code in the last argument
        if args and args[-1] in ['R', 'f', 'd', 't', 'T', 'D', 'F']:
            format_code = args.pop(-1)

        # Check for timezone in arguments
        if args:
            timezone = args.pop(-1).upper()
            if timezone == "ET":
                timezone = "America/New_York"  # Ensures ET covers both EST and EDT
            
        # If no specific date/time is provided, use the current time in the specified timezone
        date_str = args[0] if args else ""
        target_time = parse_datetime(date_str, now, timezone)

        # Convert target time to UTC for the Discord timestamp
        unix_timestamp = int(target_time.astimezone(pytz.utc).timestamp())
        discord_timestamp = f"<t:{unix_timestamp}:{format_code}>"

        # Display the expected time in the requested timezone with proper label
        formatted_expected_time = target_time.strftime("%Y-%m-%d %I:%M %p %Z")  # Ensures timezone abbreviation displays
        response = f"**Expected time**: {formatted_expected_time}\n**Timestamp**: {discord_timestamp}"

        await message.channel.send(response)

    except Exception as e:
        await message.channel.send("An error occurred while processing your request.")

import datetime
import pytz

def parse_datetime(date_str, now, timezone):
    """
    Parses a date-time string, filling missing parts with defaults and localizing to timezone.
    """
    tz = pytz.timezone(timezone) if timezone in pytz.all_timezones else pytz.utc

    try:
        # If no date_str provided, return current time in specified timezone
        if not date_str:
            return now.astimezone(tz)

        date_str = date_str.strip().lower().replace(" ", "")
        is_pm = date_str.endswith("pm") or date_str.endswith("p")
        is_am = date_str.endswith("am") or date_str.endswith("a")

        if is_am or is_pm:
            date_str = date_str.replace("am", "").replace("pm", "").replace("a", "").replace("p", "")
            hour = int(date_str.split(":")[0]) if ":" in date_str else int(date_str)
            minute = int(date_str.split(":")[1]) if ":" in date_str else 0
            if is_pm:
                hour = hour % 12 + 12
            dt = datetime.datetime(now.year, now.month, now.day, hour, minute)

        elif len(date_str) == 5 and date_str.count("-") == 1:
            dt = datetime.datetime.strptime(f"{now.year}-{date_str}", "%Y-%m-%d")
            dt = dt.replace(hour=now.hour, minute=now.minute)

        elif len(date_str) == 7:
            dt = datetime.datetime.strptime(date_str + "-01", "%Y-%m-%d")
            dt = dt.replace(hour=0, minute=0)

        elif len(date_str) == 4:
            dt = datetime.datetime(int(date_str), 1, 1, 0, 0)

        elif len(date_str) == 10:
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            dt = dt.replace(hour=now.hour, minute=now.minute)

        elif "T" in date_str:
            dt = datetime.datetime.fromisoformat(date_str)

        elif len(date_str) == 2:
            hour = int(date_str)
            dt = datetime.datetime(now.year, now.month, now.day, hour, 0)

        elif len(date_str) == 5:
            hour, minute = map(int, date_str.split(":"))
            dt = datetime.datetime(now.year, now.month, now.day, hour, minute)

        else:
            dt = now

        if dt.tzinfo is None:
            dt = tz.localize(dt, is_dst=None)

        return dt

    except Exception as e:
        return now
