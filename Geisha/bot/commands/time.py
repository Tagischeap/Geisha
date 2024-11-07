# commands/time.py

from datetime import datetime as dt
import pytz
import re
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

# Map common timezone abbreviations to full names
timezone_abbreviations = {
    'UTC': 'UTC', 'GMT': 'Europe/London', 'BST': 'Europe/London',
    'EST': 'America/New_York', 'EDT': 'America/New_York',
    'CST': 'America/Chicago', 'CDT': 'America/Chicago',
    'MST': 'America/Denver', 'MDT': 'America/Denver',
    'PST': 'America/Los_Angeles', 'PDT': 'America/Los_Angeles',
    'AKST': 'America/Anchorage', 'AKDT': 'America/Anchorage',
    'HST': 'Pacific/Honolulu',
    'AST': 'America/Halifax', 'ADT': 'America/Halifax',
    'NST': 'America/St_Johns', 'NDT': 'America/St_Johns',
    'ART': 'America/Argentina/Buenos_Aires',
    'BRT': 'America/Sao_Paulo',
    'COT': 'America/Bogota',
    'MEX': 'America/Mexico_City',
    'CLT': 'America/Santiago',
    'GMT+1': 'Europe/Paris', 'CET': 'Europe/Paris', 'CEST': 'Europe/Berlin',
    'EET': 'Europe/Athens', 'EEST': 'Europe/Athens',
    'MSK': 'Europe/Moscow',
    'IST': 'Asia/Kolkata',
    'PKT': 'Asia/Karachi',
    'BST': 'Asia/Dhaka',
    'ICT': 'Asia/Bangkok',
    'WIB': 'Asia/Jakarta',
    'SGT': 'Asia/Singapore',
    'CST': 'Asia/Taipei',
    'HKT': 'Asia/Hong_Kong',
    'JST': 'Asia/Tokyo',
    'KST': 'Asia/Seoul',
    'ACST': 'Australia/Adelaide', 'ACDT': 'Australia/Adelaide',
    'AEST': 'Australia/Sydney', 'AEDT': 'Australia/Sydney',
    'AWST': 'Australia/Perth',
    'NZST': 'Pacific/Auckland', 'NZDT': 'Pacific/Auckland',
    'SAST': 'Africa/Johannesburg',
    'EAT': 'Africa/Nairobi',
    'WAT': 'Africa/Lagos',
    'CAT': 'Africa/Harare',
    'WET': 'Europe/Lisbon', 'WEST': 'Europe/Lisbon'
}

async def execute(client, message, args):
    try:
        now = dt.now(pytz.utc)
        format_code = "t"  # Default format code

        # Check if there are no arguments
        if not args:
            # Get the current time in different US time zones
            est_time = now.astimezone(pytz.timezone("America/New_York"))
            cst_time = now.astimezone(pytz.timezone("America/Chicago"))
            pst_time = now.astimezone(pytz.timezone("America/Los_Angeles"))

            # Create the Discord timestamp for the current UTC time
            unix_timestamp = int(now.timestamp())
            discord_timestamp = f"<t:{unix_timestamp}:{format_code}>"

            # Build the response message
            response = (
                f"The time is currently: {discord_timestamp}\n"
                f"```{est_time.strftime('%I:%M %p %Z')}\n"
                f"{cst_time.strftime('%I:%M %p %Z')}\n"
                f"{pst_time.strftime('%I:%M %p %Z')}```"
            )

            # Send the message to Discord
            await message.channel.send(response)
            return

        # Process the arguments if provided
        timezone = "UTC"  # Default timezone
        date_str = args[0] if args else ""

        # Check for a format code in the last argument
        if args and args[-1].upper() in ['R', 'f', 'd', 't', 'T', 'D', 'F']:
            format_code = args.pop(-1).upper()

        # Check if the remaining argument is a timezone or an abbreviation
        if args:
            potential_timezone = args[-1].upper()
            if potential_timezone in pytz.all_timezones:
                timezone = potential_timezone
                args.pop(-1)
            elif potential_timezone in timezone_abbreviations:
                timezone = timezone_abbreviations[potential_timezone]
                args.pop(-1)

        # Parse the date and time with the provided date_str and timezone
        input_time = parse_datetime(date_str, now, timezone)

        # Convert input_time to UTC for the Discord timestamp
        utc_converted_time = input_time.astimezone(pytz.utc)
        unix_timestamp = int(utc_converted_time.timestamp())
        discord_timestamp = f"<t:{unix_timestamp}:{format_code}>"

        # Display the formatted times
        formatted_input_time = input_time.strftime("%Y-%m-%d %I:%M %p %Z")
        formatted_converted_time = utc_converted_time.strftime("%Y-%m-%d %I:%M %p UTC")
        response = (
            f"**Input Time**: {formatted_input_time}\n"
            f"**Converted Time**: {formatted_converted_time}\n"
            f"**Timestamp**: {discord_timestamp}"
        )

        await message.channel.send(response)

    except Exception as e:
        print(f"Error in execute function: {e}")
        await message.channel.send("An error occurred while processing your request. Please check your format and try again.")

def parse_datetime(date_str, now, timezone):
    """
    Parses a date-time string, filling missing parts with defaults and localizing to timezone.
    """
    tz = pytz.timezone(timezone) if timezone in pytz.all_timezones else pytz.utc
    dt_parsed = now.replace(tzinfo=None)  # Start with a naive datetime
    parsed_successfully = False  # Track if parsing succeeded
    print(f"Initial input date_str: {date_str}, now: {now}, timezone: {timezone}")

    try:
        # If no date string is provided, return current time localized to timezone
        if not date_str:
            dt_parsed = now.astimezone(tz)
            print(f"Localized current time to timezone {timezone}: {dt_parsed}")
            return dt_parsed

        # Define date formats to check sequentially
        date_formats = [
            "%Y-%m-%dT%H:%M",  # ISO format with time
            "%Y-%m-%d",        # Year-Month-Day
            "%Y-%m",           # Year-Month
            "%m-%d",           # Month-Day
            "%H:%M",           # Hour:Minute
            "%H"               # Hour only
        ]

        # Try parsing the date_str with each format
        for fmt in date_formats:
            try:
                dt_parsed = dt.strptime(date_str, fmt)
                parsed_successfully = True
                print(f"Parsed datetime using format '{fmt}': {dt_parsed}")
                # For MM-DD, assume current year if not provided
                if fmt == "%m-%d":
                    dt_parsed = dt_parsed.replace(year=now.year, hour=now.hour, minute=now.minute)
                elif fmt == "%Y-%m":
                    dt_parsed = dt_parsed.replace(day=1, hour=0, minute=0)
                break  # Exit loop on successful parse
            except ValueError:
                continue  # Try next format if this one fails

        # Only handle AM/PM if no other parsing succeeded
        if not parsed_successfully:
            am_pm_match = re.match(r"(\d{1,2})(?::(\d{2}))?\s?(AM|PM)?", date_str, re.IGNORECASE)
            if am_pm_match:
                hour = int(am_pm_match.group(1))
                minute = int(am_pm_match.group(2)) if am_pm_match.group(2) else 0
                if am_pm_match.group(3):  # Adjust for AM/PM
                    if am_pm_match.group(3).upper() == "PM" and hour != 12:
                        hour += 12  # Convert PM hour to 24-hour format
                    elif am_pm_match.group(3).upper() == "AM" and hour == 12:
                        hour = 0  # Convert 12 AM to 0:00 (midnight)
                dt_parsed = dt_parsed.replace(year=now.year, month=now.month, day=now.day, hour=hour, minute=minute)
                print(f"Parsed AM/PM time: {dt_parsed}")

        # Localize the parsed datetime to the specified timezone if it's naive
        if dt_parsed.tzinfo is None:
            dt_parsed = tz.localize(dt_parsed, is_dst=None)
            print(f"Localized datetime to timezone {timezone}: {dt_parsed}")

        return dt_parsed  # Return localized time in specified timezone

    except Exception as e:
        print(f"Error in parse_datetime: {e}")
        return now
