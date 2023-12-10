import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

 # load all the variables from the env file
load_dotenv()

bot = commands.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

# load our cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        print(f"Loaded {filename}")

# subgroup cogs


@bot.slash_command(name = "hello", description = "Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Hey!")

bot.run(os.getenv("token")) # get the token from the env file