import discord
import discord.ui

class AddMember(discord.ui.Modal):
    def __init__(self, ticket_id, ticket_class, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ticket_id = ticket_id
        self.ticket_class = ticket_class
        self.add_item(discord.ui.InputText(label="Member ID"))

    async def callback(self, interaction: discord.Interaction):
        # reference the user_id from the input
        user_id = self.children[0].value

        # check if the user is a real user
        user = await self.ticket_class.find_user(user_id)
        if user == True:
            await self.ticket_class.add_member_to_ticket(self.ticket_id, user_id)

            await interaction.response.send_message("Added member.")
        else:
            await interaction.response.send_message("User not found.")
