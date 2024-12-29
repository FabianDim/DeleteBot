from code import interact
import discord
from discord.ext import commands
from discord import app_commands, guild
import sys
import os
from dotenv import load_dotenv
from Logger import Logger

# Explicitly specify the path to the .env file
dotenv_path = 'C:\\Repos\\DeleteBot\\Key.env'
load_dotenv(dotenv_path)

class MyClient(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        try:
            GUILD_ID = discord.Object(id=320425715310788618)
            synced = await self.tree.sync(guild=GUILD_ID)
            print(f'sync {len(synced)} commands to guild')
        except Exception as e:
            print(f'error syncing {e}')
    async def on_message(self, message):
        if message.author == self.user:
            return

handler = Logger.handler
key = os.getenv('DISCORD_KEY')

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(command_prefix="!", intents = intents)
GUILD_ID = discord.Object(id=320425715310788618)

@client.tree.command(name="hello", description="Say Hello!", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message("Hi there!")

client.run(key, log_handler=handler)