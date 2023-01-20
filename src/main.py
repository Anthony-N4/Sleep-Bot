import discord, asyncio
import os
from dotenv import load_dotenv
from discord import Option
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("GUILD_ID")
bot = commands.Bot(activity = discord.Activity(type = discord.ActivityType.watching, name = "you not sleep ._."), status = discord.Status.online)

#Ugliest method, goal: get it working
def timeSlept(starting_time, ending_time) -> int:
    """Calculates the total amount of time user slept
    
    Args: 
        starting_time(str), ending_time(str): starting and ending timestamps

    Returns:
       int: Converted to str, how much time has passed between timestamps 
    """
    #Uppercase the AM and PM in user input
    starting_time = starting_time.upper()
    ending_time = ending_time.upper()

    #Splits the hours from the minutes
    startHour_String = starting_time.split(':')[0]
    startMin_String = starting_time.split(':')[-1]
    endHour_String = ending_time.split(':')[0]
    endMin_String = ending_time.split(':')[-1]

    #Converts the hours and minutes into integers
    startHour = int(startHour_String)
    startMin = int(startMin_String[:-2])
    endHour = int(endHour_String)
    endMin = int(endMin_String[:-2])

    #Converts the time into 24 hr format
    if "PM" in startMin_String and startHour >= 1 and startHour < 12:
        startHour = startHour + 12
    elif "AM" in startMin_String and startHour == 12:
        #If the time is 12:00AM, in 24 hr format, time is 0:00
        startHour = 0
        
    if "PM" in endMin_String and endHour >= 1 and endHour < 12:
        endHour = endHour + 12
    elif "AM" in endMin_String and endHour == 12:
        #If the time is 12:00AM, in 24 hr format, time is 0:00
        endHour = 0

    #Calculates time passed
    #If startHour is PM and endHour is AM
    if startHour > 12 and endHour < 12:
        totalHours = ((24 - startHour) + endHour) - 1
        totalMins = (60 - startMin) + endMin
    
    #Sleep is shorter than 1 hour
    elif startHour == endHour:
        totalHours = 0
        totalMins = endMin - startMin

    #If both times are PM and sleep atleast 12 hours
    elif ((startHour and endHour > 12) and startHour > endHour):
        totalHours = ((24 - startHour) + endHour) -1
        totalMins = (60 - startMin) + endMin

    #If both times are AM and sleep atleast 12 hours
    elif ((startHour and endHour < 12) and startHour > endHour):
        totalHours = ((24 - startHour) + endHour) -1
        totalMins = (60 - startMin) + endMin
   
    else:
        totalHours = (endHour - startHour) - 1
        totalMins = (60 - startMin) + endMin  
    
    if totalMins == 60:
        totalHours = totalHours + 1
        totalMins = 0
 
    return str(totalHours) + " hours and " + str(totalMins) + " minutes"

@bot.slash_command(name = "log-hours", description = "Logs when you start and stop sleeping", guild_ids = [GUILD])
async def log_data(ctx, start: Option(str, description = "When did you start sleeping?", require = True), end: Option(str, description = "When did you wake up?")):

    await ctx.respond(f"Hours recorded. You slept from {start} to {end}, a total of " + timeSlept(start, end) + "." " Nice!")

@bot.slash_command(name = "weekly-average", description = "Returns the average amount of sleep you got this week", guild_ids = [GUILD])
async def log_data(ctx):
    await ctx.respond("Test")

@bot.slash_command(name = "graph", description = "Returns a graph of how much sleep you got this month", guild_ids = [GUILD])
async def log_data(ctx):
    await ctx.respond("Test")
 
bot.run(TOKEN)