import discord
import os
from dotenv import load_dotenv
from discord import Option
from discord.ext import commands


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(activity = discord.Activity(type = discord.ActivityType.watching, name = "ou not sleep"), status = discord.Status.online)

@bot.slash_command(name = "log-hours", description = "Logs when you start and stop sleeping", guild_ids = [965992554246049833])
async def log_data(ctx, start: Option(str, description = "When did you start sleeping?", require = True), end: Option(str, description = "When did you wake up?")):
    await ctx.respond(f"Hours recorded. You slept from {start} to {end}. Nice!")

@bot.slash_command(name = "weekly-average", description = "Returns the average amount of sleep you got this week", guild_ids = [965992554246049833])
async def log_data(ctx):
    await ctx.respond("Test")

@bot.slash_command(name = "graph", description = "Returns a graph of how much sleep you got this month", guild_ids = [965992554246049833])
async def log_data(ctx):
    await ctx.respond("Test")

 
bot.run(TOKEN)