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
    Parses a date-time string and fills in missing parts with defaults.
    Adjusts for timezone.
    """
    tz = pytz.timezone(timezone) if timezone in pytz.all_timezones else pytz.utc

    try:
        # Handle AM/PM times first
        date_str = date_str.strip().lower().replace(" ", "")
        is_pm = date_str.endswith("pm") or date_str.endswith("p")
        is_am = date_str.endswith("am") or date_str.endswith("a")

        if is_am or is_pm:
            # Remove 'am', 'pm', 'a', 'p' suffix for consistent parsing
            date_str = date_str.replace("am", "").replace("pm", "").replace("a", "").replace("p", "")

            # Parse hour and minute from cleaned date_str
            if ":" in date_str:
                hour, minute = map(int, date_str.split(":"))
            else:
                hour = int(date_str)
                minute = 0

            # Adjust hour for PM, keeping 12 PM as 12 and converting 1 PM - 11 PM appropriately
            if is_pm:
                hour = hour % 12 + 12
            elif is_am:
                hour = hour % 12  # Ensures 12 AM becomes 0 for midnight

            dt = datetime.datetime(now.year, now.month, now.day, hour, minute, 0)

        elif len(date_str) == 5 and date_str.count("-") == 1:  # Format MM-DD
            dt = datetime.datetime.strptime(f"{now.year}-{date_str}", "%Y-%m-%d")
            dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)

        elif len(date_str) == 7:  # Format YYYY-MM
            dt = datetime.datetime.strptime(date_str + "-01", "%Y-%m-%d")
            dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)

        elif len(date_str) == 4:  # Format YYYY
            dt = datetime.datetime(int(date_str), 1, 1, 0, 0, 0)

        elif len(date_str) == 10:  # Format YYYY-MM-DD
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)

        elif "T" in date_str:  # Full date and time, e.g., YYYY-MM-DDTHH:MM
            dt = datetime.datetime.fromisoformat(date_str)

        elif len(date_str) == 2:  # Only hour provided (HH)
            hour = int(date_str)
            dt = datetime.datetime(now.year, now.month, now.day, hour, 0, 0)

        elif len(date_str) == 5:  # Only time provided (HH:MM)
            hour, minute = map(int, date_str.split(":"))
            dt = datetime.datetime(now.year, now.month, now.day, hour, minute, 0)

        else:
            dt = now  # Default to current time if no recognized date format provided

        # Only localize if dt is naive (i.e., no timezone information)
        if dt.tzinfo is None:
            dt = tz.localize(dt, is_dst=None)

        return dt  # Return localized time in specified timezone

    except Exception as e:
        return now  # Default to current UTC time in case of an error