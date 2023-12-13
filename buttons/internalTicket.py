import discord
import discord.ui
from discord.ext import commands
from menus.addMember import AddMember
from menus.removeMember import RemoveMember
class InternalTicket(discord.ui.View):
    def __init__(self, ticket_id, ticket_class):
        super().__init__()
        self.ticket_id = ticket_id
        self.ticket_class = ticket_class

    @discord.ui.button(label="Close", style=discord.ButtonStyle.red, custom_id="close_ticket")
    async def close_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
         # Close the ticket
        await self.ticket_class.close_ticket(self.ticket_id)
        await interaction.response.send_message("Ticket closed.")

    @discord.ui.button(label="Copy ID", style=discord.ButtonStyle.blurple, custom_id="copy_id")
    async def copy_id_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Copy the ticket ID to the clipboard
        await self.bot.copy_to_clipboard(self.ticket_id)
        await interaction.response.send_message("Ticket ID copied to clipboard.")

    @discord.ui.button(label="Add Member", style=discord.ButtonStyle.green, custom_id="add_member")
    async def add_member_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            await interaction.response.send_modal(AddMember(title="Add Member", ticket_id=self.ticket_id, ticket_class=self.ticket_class))
        except discord.InteractionResponded:
            await interaction.response.send_message("You already have a modal open!", ephemeral=True)

    @discord.ui.button(label="Remove Member", style=discord.ButtonStyle.red, custom_id="remove_member")
    async def remove_member_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            await interaction.response.send_modal(RemoveMember(title="Remove Member", ticket_id=self.ticket_id, ticket_class=self.ticket_class))
        except discord.InteractionResponded:
            await interaction.response.send_message("You already have a modal open!", ephemeral=True)

