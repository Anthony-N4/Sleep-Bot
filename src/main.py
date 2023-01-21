import discord, asyncio
import os
import requests
import json
from collections import namedtuple
from dotenv import load_dotenv
from discord import Option
from discord.ext import commands


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("GUILD_ID")
CHANNEL = os.getenv("CHANNEL_ID")
AUTH = os.getenv("AUTHORIZATION")
REQUEST = os.getenv("REQUETS_URL")

bot = commands.Bot(
    activity = discord.Activity(type = discord.ActivityType.watching, name = "you not sleep ._."),
    status = discord.Status.online)

Time = namedtuple('Time', ['hour', 'minutes', 'indicator'])

def parse_time(time_str: str) -> Time:
    """Parses a 12-hour time into the hour, minutes, and PM/AM.
    This assumes user puts a : between hour and minutes and has 'PM' or 'AM' at the end."""

    if time_str.startswith('-'):
        raise ValueError

    time_str = time_str.replace(' ', '')
    hour = int(time_str.split(':')[0])
    minute = int(time_str.split(':')[1][:-2])

    return Time(hour, minute, time_str.split(':')[1][-2:])

def convert_to_24_hour(starting_time: Time, ending_time: Time) -> tuple[Time, Time]:
    """Converts to 24-hour time"""

    if starting_time.indicator.upper() == 'PM' and starting_time[0] != 12:
        starting_time = Time(starting_time.hour + 12, starting_time.minutes, '24')

    if ending_time.indicator.upper() == 'PM' and ending_time[0] != 12:
        ending_time = Time(ending_time.hour + 12, ending_time.minutes, '24')

    if starting_time.indicator.upper() == 'AM' and starting_time[0] == 12:
        starting_time = Time(starting_time.hour - 12, starting_time.minutes, '24')
    
    if ending_time.indicator.upper() == 'AM' and ending_time[0] == 12:
        ending_time = Time(ending_time.hour - 12, ending_time.minutes, '24')

    return starting_time, ending_time

def find_time_slept(times: tuple[Time, Time]) -> tuple[int, int]:
    """Finds the amount of time slept in hours and minutes."""
    start, end = times

    # Assumes slept from one day to next
    if start.hour > end.hour:
        total_hours = 24 - start.hour + end.hour
    else:
        total_hours = end.hour - start.hour

    if end.minutes >= start.minutes:
        total_minutes = end.minutes - start.minutes
    else:
        total_minutes = 60 + end.minutes - start.minutes
        total_hours = total_hours - 1  

    return total_hours, total_minutes


def find_time_slept_str(time_slept: tuple[int, int]):
    hours, minutes = time_slept
    time_string = 'You slept for'

    if hours == 0 and minutes == 0:
        return 'Take some melatonin gummies'

    if hours != 0:
        time_string += f' {hours} hour(s)'

    if minutes != 0:
        time_string += f' {minutes} minute(s)'
    
    if hours < 3:
        time_string += '. Yikes ... :grimacing:'
    
    else:
        time_string += ". Nice! <:jac1:773612390604210227><:jac2:773612349957341204><:jac3:773612364096340029>"

    return time_string

def execute_time_routine(start_str: str, end_str: str) -> str:
    return find_time_slept_str(
        find_time_slept(convert_to_24_hour(parse_time(start_str), parse_time(end_str))))

def retrieve_messages(CHANNEL) -> int:
    headers = {
        'authorization': AUTH
    }
    r = requests.get(f'https://discord.com/api/v9/channels/{CHANNEL}/messages?limit=1', headers = headers)
    json_object = json.loads(r.text)
    #Looks at JSON data from most recent message sent in CHANNEL
    #Loops through JSON data, looks for nested keys 'interaction' -> 'user' -> 'id'
    #Returns userid of person who called slash command
    for value in json_object:
        print(value['interaction']['user']['id'])
    #['interaction']['user']['id']
@bot.slash_command(name = "log-hours", description = "Logs when you start and stop sleeping",
                   guild_ids = [GUILD])
async def log_data(ctx,
                   start: Option(str, description = "When did you start sleeping?", require = True),
                   end: Option(str, description = "When did you wake up?")):
    try:
        #retrieve_messages(CHANNEL)
        await ctx.respond(
            f'{start} - {end}. {execute_time_routine(start, end)}')
    except ValueError:
        await ctx.respond("You're a walking bruh moment times two.")


@bot.slash_command(name = "weekly-average",
                   description = "Returns the average amount of sleep you got this week",
                   guild_ids = [GUILD])
async def log_data(ctx):
    await ctx.respond("Test")


@bot.slash_command(name = "graph",
                   description = "Returns a graph of how much sleep you got this month",
                   guild_ids = [GUILD])
async def log_data(ctx):
    await ctx.respond("Test")


bot.run(TOKEN)
