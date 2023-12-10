import discord
from discord.ext import commands

# create the cog class
class Ping(commands.Cog):
    # initialize the class and pass in the bot
    def __init__(self, bot):
        self.bot = bot

    # create a slash command
    @discord.slash_command(description = "Check the bot's latency")
    async def ping(self, ctx):
        await ctx.respond(f"Pong! {round(self.bot.latency * 1000)}ms")

# setup function to add the cog
def setup(bot):
    bot.add_cog(Ping(bot))