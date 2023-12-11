import discord

class AddMember(discord.ui.View):
    def __init__(self, ticket_id, ticket_class):
        super().__init__()
        self.ticket_id = ticket_id
        self.ticket_class = ticket_class
        self.ticket = self.ticket_class.find_ticket(self.ticket_id)

    def create_options(self):
        options = []
        for member in self.ticket.members:
            options.append(discord.SelectOption(
                label="test",
                description=f"Pick this if you like!"
            ))
        return options

    @discord.ui.select(
        placeholder = "Choose a Flavor!",
        min_values = 1,
        max_values = 1,
        options = create_options
    )
    async def select_callback(self, select, interaction):
        await interaction.response.send_message(f"Awesome! I like {select.values[0]} too!")