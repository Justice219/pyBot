import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from util.ticket_lib import TicketsLib
from util.settings_lib import SettingsLib
from discord.ui import Button, View

class TicketCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ticket = TicketsLib(bot) # replace with your guild id
        self.settings = SettingsLib()

    ticket = SlashCommandGroup("ticket", "Ticket commands")

    @ticket.command(description="Create a ticket")
    async def create(self, ctx):
        # check if guild i

        # create the ticket
        awachannel, ticket_id = await self.ticket.create_ticket(ctx.author.id)

        # send a message
        await ctx.respond(f"Created a ticket at {awachannel.mention}")

    @ticket.command(description="Close a ticket")
    async def close(self, ctx, ticket_id: int):
        # close the ticket
        await self.ticket.close_ticket(ticket_id)

        # send a message
        await ctx.respond("Closed a ticket")

    @ticket.command(description="Clear all tickets")
    async def clear(self, ctx):
        # clear all tickets
        await self.ticket.clear_tickets()

        # send a message
        await ctx.respond("Cleared all tickets")
    
    @ticket.command(description="Finds a ticket from an id")
    async def find(self, ctx, ticket_id: int):
        # find the ticket
        ticket = await self.ticket.find_ticket(ticket_id)

        # send a message
        await ctx.respond(f"Found a ticket at {ticket.mention}")

    @commands.Cog.listener()
    async def on_application_command_error(
        self, ctx: discord.ApplicationContext, error: discord.DiscordException
    ):
        if isinstance(error, commands.NotOwner):
            await ctx.respond("You can't use that command!")
        else:
            messageEmbed = discord.Embed(
                title="Error!",
                description="Something went wrong! Ensure the bot has been setup properly.",
                color=discord.Colour.red()
            )
            trackebackEmbed = discord.Embed(
                title="Error Traceback",
                description=f"```{error}```",
                color=discord.Colour.red()
            )
            await ctx.respond(embed=messageEmbed)
            await ctx.respond(embed=trackebackEmbed)
            raise error  # Raise other errors so they aren't ignored

def setup(bot):
    bot.add_cog(TicketCommands(bot))