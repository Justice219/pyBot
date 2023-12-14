import discord
import json
import os

class SettingsLib():
    def __init__(self):
        self.keys = ["guild_id", "category_id"]
        self.guild_id = self.load_settings('guild_id')
        self.category_id = self.load_settings('category_id')
        
    def create_default_settings(self):
        # create the default settings
        settings = {}
        for key in self.keys:
            settings[key] = "None"
        # write the settings to the file
        with open('settings.json', 'w') as f:
            json.dump(settings, f, indent=4)

    def load_settings(self, key):
        settings = {}
        # if the file doesn't exist, create it
        if not os.path.exists('settings.json'):
            self.create_default_settings()

        with open('settings.json') as f:
            settings = json.load(f)
        return settings[key]
        
    def set_settings(self, key, value):
        # if the file doesn't exist, create it
        settings = {}
        if not os.path.exists('settings.json'):
            self.create_default_settings()

        with open('settings.json') as f:
            settings = json.load(f)
        settings[key] = value
        with open('settings.json', 'w') as f:
            json.dump(settings, f, indent=4)

    async def setup_settings(self, bot, ctx):
        # go through each setting and ask in chat for the value
        for key in self.keys:
            # ask for the value
            await ctx.respond(f"What is the {key}?")
            # wait for a response
            response = await bot.wait_for("message", check=lambda message: message.author == ctx.author)
            # set the value
            self.set_settings(key, response.content)
            # send a message
            await ctx.respond(f"Set the {key} to {response.content}")

        finishedEmbed = discord.Embed(
            title="Setup complete!", 
            description="Setup is complete! You can now use the bot properly.",
            color=discord.Colour.blurple()
            )
        
        # add a field for each setting
        for key in self.keys:
            finishedEmbed.add_field(name=key + ":", value=self.load_settings(key), inline=False)

        # send the embed
        await ctx.respond(embed=finishedEmbed)
        await ctx.respond("Setup complete!")