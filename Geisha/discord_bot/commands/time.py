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
        if args and args[-1].upper() in ['R', 'f', 'd', 't', 'T', 'D', 'F']:
            format_code = args.pop(-1).upper()

        # Check for timezone in the second-to-last argument if date/time is provided
        if args and args[-1] in pytz.all_timezones:
            timezone = args.pop(-1).upper()

        # Set date_str to remaining argument or default to empty string
        date_str = args[0] if args else ""
        print(f"Parsed date_str: {date_str}, timezone: {timezone}, format_code: {format_code}")

        # Parse the date and time with the provided date_str and timezone
        target_time = parse_datetime(date_str, now, timezone)

        # Convert target time to UTC for the Discord timestamp
        unix_timestamp = int(target_time.astimezone(pytz.utc).timestamp())
        discord_timestamp = f"<t:{unix_timestamp}:{format_code}>"

        # Display the expected time in the requested timezone with proper label
        formatted_expected_time = target_time.strftime("%Y-%m-%d %I:%M %p %Z")
        response = f"**Expected time**: {formatted_expected_time}\n**Timestamp**: {discord_timestamp}"

        await message.channel.send(response)

    except Exception as e:
        await message.channel.send("An error occurred while processing your request.")

def parse_datetime(date_str, now, timezone):
    """
    Parses a date-time string, filling missing parts with defaults and localizing to timezone.
    """
    tz = pytz.timezone(timezone) if timezone in pytz.all_timezones else pytz.utc
    dt = now  # Default to current time
    print(f"Initial input date_str: {date_str}, now: {now}, timezone: {timezone}")

    try:
        # Handle explicit ISO format (YYYY-MM-DDTHH:MM) directly using strptime
        if date_str and "T" in date_str:
            try:
                print(f"Attempting ISO format parse for: {date_str}")
                dt = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
                print(f"Parsed ISO datetime: {dt}")
            except ValueError:
                print(f"Failed ISO parse for {date_str}, continuing to other formats.")

        # Check for AM/PM or single hour formats
        elif date_str:
            date_str = date_str.strip().lower().replace(" ", "")
            print(f"Processed date_str for AM/PM and space removal: {date_str}")

            is_pm = date_str.endswith("pm") or date_str.endswith("p")
            is_am = date_str.endswith("am") or date_str.endswith("a")
            print(f"is_pm: {is_pm}, is_am: {is_am}")

            if is_am or is_pm:
                date_str = date_str.replace("am", "").replace("pm", "").replace("a", "").replace("p", "")
                hour = int(date_str.split(":")[0]) if ":" in date_str else int(date_str)
                minute = int(date_str.split(":")[1]) if ":" in date_str else 0
                if is_pm:
                    hour = hour % 12 + 12
                dt = datetime.datetime(now.year, now.month, now.day, hour, minute)
                print(f"Parsed AM/PM time: {dt}")

            # Handle month-day format (MM-DD)
            elif len(date_str) == 5 and date_str.count("-") == 1:
                print(f"Attempting MM-DD format parse for: {date_str}")
                dt = datetime.datetime.strptime(f"{now.year}-{date_str}", "%Y-%m-%d")
                dt = dt.replace(hour=now.hour, minute=now.minute)
                print(f"Parsed MM-DD date: {dt}")

            # Handle year-month format (YYYY-MM)
            elif len(date_str) == 7:
                print(f"Attempting YYYY-MM format parse for: {date_str}")
                dt = datetime.datetime.strptime(date_str + "-01", "%Y-%m-%d")
                dt = dt.replace(hour=0, minute=0)
                print(f"Parsed YYYY-MM date: {dt}")

            # Handle year-only format (YYYY)
            elif len(date_str) == 4:
                print(f"Attempting YYYY format parse for: {date_str}")
                dt = datetime.datetime(int(date_str), 1, 1, 0, 0)
                print(f"Parsed YYYY date: {dt}")

            # Handle year-month-day format (YYYY-MM-DD)
            elif len(date_str) == 10:
                print(f"Attempting YYYY-MM-DD format parse for: {date_str}")
                dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                dt = dt.replace(hour=now.hour, minute=now.minute)
                print(f"Parsed YYYY-MM-DD date: {dt}")

            # Handle hour only (HH)
            elif len(date_str) == 2 and date_str.isdigit():
                print(f"Attempting HH format parse for: {date_str}")
                hour = int(date_str)
                dt = datetime.datetime(now.year, now.month, now.day, hour, 0)
                print(f"Parsed HH time: {dt}")

            # Handle hour and minute (HH:MM)
            elif len(date_str) == 5:
                print(f"Attempting HH:MM format parse for: {date_str}")
                hour, minute = map(int, date_str.split(":"))
                dt = datetime.datetime(now.year, now.month, now.day, hour, minute)
                print(f"Parsed HH:MM time: {dt}")

        # Localize the parsed time to the specified timezone
        if dt.tzinfo is None:
            dt = tz.localize(dt, is_dst=None)
            print(f"Localized datetime to timezone {timezone}: {dt}")

        return dt  # Return localized time in specified timezone

    except Exception as e:
        print(f"Error in parse_datetime: {e}")
        return now
