import os 
import json
import discord
from discord.ext import commands
from buttons.internalTicket import InternalTicket

class TicketsLib:
    def __init__(self, bot):
        self.bot = bot
        self.guild_id = self.load_settings('guild_id')
        self.category_id = self.load_settings('category_id')
        self.ticket_data = self.get_ticket_data()

    def load_settings(self, key):
        with open('settings.json') as f:
            settings = json.load(f)
        return settings[key]
    
    def get_ticket_data(self):
        # if the file doesn't exist, create it
        if not os.path.exists('tickets.json'):
            with open('tickets.json', 'w') as f:
                json.dump({}, f, indent=4)
        with open('tickets.json') as f:
            ticket_data = json.load(f)
        return ticket_data
    
    def write_ticket_data(self):
        with open('tickets.json', 'w') as f:
            json.dump(self.ticket_data, f, indent=4)

    def create_unique_ticket_id(self):
        # simple hash generator
        ticket_id = 0
        for i in range(0, 10):
            ticket_id += ord(os.urandom(1))
        return ticket_id
    
    async def clear_tickets(self):
        # delete all channels
        guild = await self.bot.fetch_guild(self.guild_id)
        if guild is None:
            print("Error: Guild not found.")
            print("Guild ID:", self.guild_id)
            return None
        
        category = await guild.fetch_channel(self.category_id)
        if category is None:
            print("Error: Category not found.")
            print("Category ID:", self.category_id)
            return None
        
        for channel in category.channels:
            await channel.delete()
    
        # reset settings
        self.guild_id = self.load_settings('guild_id')
        self.category_id = self.load_settings('category_id')

        # clear the ticket data
        self.ticket_data = {}
        self.write_ticket_data()

    async def send_ticket_message(self, channel, ticket_id, ticket_class):
        # create the embed
        embed = discord.Embed(
            title="Ticket: " + str(ticket_id),
            description="Support will be with you shortly!",
            color=discord.Colour.blurple(),
        )
                
        # send the message
        await channel.send(embed=embed, view=InternalTicket(ticket_id, ticket_class))

    async def set_ticket_permissions(self, channel, user_id):
        # get the user
        guild = await self.bot.fetch_guild(self.guild_id)

        if guild is None:
            print("Error: Guild not found.")
            print("Guild ID:", self.guild_id)
            return None
        
        user = await guild.fetch_member(user_id)
        if user is None:
            print("Error: User not found.")
            print("User ID:", user_id)
            return None
        
        # set the permissions
        await channel.set_permissions(user, read_messages=True, send_messages=True)
        await channel.set_permissions(guild.default_role, read_messages=False, send_messages=False)
        await channel.set_permissions(self.bot.user, read_messages=True, send_messages=True)

    async def add_member_to_ticket(self, ticket_id, user_id):
        # update the ticket data
        ticket = await self.find_ticket(ticket_id)
        if ticket is None:
            print("Error: Ticket not found.")
            print("Ticket ID:", ticket_id)
            return None
        
        ticket_data = self.ticket_data[self.guild_id][ticket_id]
        ticket_data['members'].append(user_id)
        self.write_ticket_data()

        # allow the user to see the channel
        channel_id = self.ticket_data[self.guild_id][ticket_id]['channel_id']
        channel = await self.bot.fetch_channel(channel_id)

        if channel is None:
            print("Error: Channel not found.")
            print("Channel ID:", channel_id)
            return None
        
        user = await self.bot.fetch_user(user_id)
        if user is None:
            print("Error: User not found.")
            print("User ID:", user_id)
            return None
        
        await channel.set_permissions(user, read_messages=True, send_messages=True)

    async def remove_member_from_ticket(self, ticket_id, user_id):
        # update the ticket data
        ticket = await self.find_ticket(ticket_id)
        if ticket is None:
            print("Error: Ticket not found.")
            print("Ticket ID:", ticket_id)
            return None
        
        ticket_data = self.ticket_data[self.guild_id][ticket_id]
        ticket_data['members'].remove(user_id)
        self.write_ticket_data()

        # allow the user to see the channel
        channel_id = self.ticket_data[self.guild_id][ticket_id]['channel_id']
        channel = await self.bot.fetch_channel(channel_id)

        if channel is None:
            print("Error: Channel not found.")
            print("Channel ID:", channel_id)
            return None
        
        user = await self.bot.fetch_user(user_id)
        if user is None:
            print("Error: User not found.")
            print("User ID:", user_id)
            return None
        
        await channel.set_permissions(user, read_messages=False, send_messages=False)

    async def find_user(self, user_id):
        user = None
        guild = await self.bot.fetch_guild(self.guild_id)
        if guild is None:
            print("Error: Guild not found.")
            print("Guild ID:", self.guild_id)
            return False, None
        
        try:
            user = await guild.fetch_member(user_id)
        except discord.errors.HTTPException:
            print("Error: User not found.")
            print("User ID:", user_id)
            return False, None
        
        return True

    async def find_ticket(self, ticket_id):
        # get the guild
        guild = await self.bot.fetch_guild(self.guild_id)
        if guild is None:
            print("Error: Guild not found.")
            print("Guild ID:", self.guild_id)
            return None
        
        data = self.get_ticket_data()
        if data is None:
            print("Error: Ticket data not found.")
            return None
        
        channel_id = data[self.guild_id][str(ticket_id)]['channel_id']
        if channel_id is None:
            print("Error: Channel ID not found.")
            return None
        
        channel = await guild.fetch_channel(channel_id)
        return channel
    
    async def get_ticket(self, ticket_id):
        guild = await self.bot.fetch_guild(self.guild_id)
        if guild is None:
            print("Error: Guild not found.")
            print("Guild ID:", self.guild_id)
            return None
        
        channel = discord.utils.get(guild.channels, name=f'ticket-{ticket_id}')
        if channel is None:
            print("Error: Channel not found.")
            print("Channel ID:", ticket_id)
            return None
        
        return channel

    async def create_ticket(self, user_id):
        # get the guild
        guild = await self.bot.fetch_guild(self.guild_id)
        if guild is None:
            print("Error: Guild not found.")
            print("Guild ID:", self.guild_id)
            return None

        # get the category
        category = await guild.fetch_channel(self.category_id)
        if category is None:
            print("Error: Category not found.")
            print("Category ID:", self.category_id)
            return None

        # create the ticket id
        ticket_id = self.create_unique_ticket_id()

        # update the ticket data
        self.ticket_data.setdefault(self.guild_id, {})
        self.ticket_data[self.guild_id][ticket_id] = {
            'user_id': user_id,
            'ticket_id': ticket_id,
            'channel_id': None,
            'members': []
        }
        self.write_ticket_data()

        try:
            # create the channel
            channel = await guild.create_text_channel(f'ticket-{ticket_id}', category=category)
            
            # update the ticket data with our new channel id
            self.ticket_data[self.guild_id][ticket_id]['channel_id'] = channel.id
            self.write_ticket_data()

            # set the permissions
            await self.set_ticket_permissions(channel, user_id)

            # send the ticket message
            await self.send_ticket_message(channel, ticket_id, self)

            # return the channel and ticket id
            return channel, ticket_id
        
        # if the bot doesn't have permission to create channels, return None
        except discord.Forbidden:
            # if the bot doesn't have permission to create channels, return None
            print("Error: Bot does not have permission to create text channels.")
            return None
        
    async def close_ticket(self, ticket_id):
        guild = await self.bot.fetch_guild(self.guild_id)
        if guild is None:
            print("Error: Guild not found.")
            print("Guild ID:", self.guild_id)
            return None
        
        category = await guild.fetch_channel(self.category_id)
        if category is None:
            print("Error: Category not found.")
            print("Category ID:", self.category_id)
            return None
        
        channel = await self.find_ticket(ticket_id)
        if channel is None:
            print("Error: Channel not found.")
            print("Channel ID:", ticket_id)
            return None
        
        # delete the channel
        await channel.delete()

        # delete the ticket data
        del self.ticket_data[self.guild_id][ticket_id]
        self.write_ticket_data()
        