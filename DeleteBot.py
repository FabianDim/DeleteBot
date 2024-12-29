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

@client.tree.command(name="ping", description="If I am here I will say Pang!", guild=GUILD_ID) #developing / commands for the 
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message("pang")

@client.tree.command(name="delete_messages", description="Specify a phrase and how much you want to delete andI will delete that many messages", guild=GUILD_ID)
async def deleteMessages(interaction: discord.Interaction, phrase: str, amount: int):
    counter = 0
    async for message in channel.history(limit=amount):
        if(message.author == client.user):
            counter+=1
    await
client.run(key, log_handler=handler)