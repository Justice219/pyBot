import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from util.settings_lib import SettingsLib

class SetupCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.settings = SettingsLib()

    # permission check
    @commands.has_permissions(administrator=True)
    @discord.slash_command(description = "Setup the bot")
    async def setup(self, ctx):
        await self.settings.setup_settings(self.bot, ctx)

def setup(bot):
    bot.add_cog(SetupCommand(bot))