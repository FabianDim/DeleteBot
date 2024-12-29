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
badWords = [str(os.getenv('BadWord1')),str(os.getenv('BadWord2')),str(os.getenv('BadWord3')),str(os.getenv('BadWord4'))]

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(command_prefix="!", intents = intents)
GUILD_ID = discord.Object(id=320425715310788618)

@client.tree.command(name="ping", description="If I am here I will say Pang!", guild=GUILD_ID) #developing / commands for the 
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message("pang")

@client.tree.command(name="delete_messages", description="Specify a phrase and how many messages you want to find and then specify whether you want them deleted", guild=GUILD_ID)
async def findMessages(interaction: discord.Interaction, phrase: str, amount: int):
    await interaction.response.defer()  # Defer the response to avoid timeout

    counter = 0

    if amount < 0 or amount >= 1000:
        await interaction.followup.send(f"Please limit the search radius to 5000")#avoid to many messages taking to long.
        return

    channel = interaction.channel
    messages = [message async for message in channel.history(limit=amount)]#creates an array of messages
    counter = sum(1 for message in messages if phrase in message.content) #counts messages with phrases.
    
    if badWords.__contains__(phrase): #would like to have used a pointer here to be able to reference the location of it so i dont have to change phrase
        phrase = "REDACTED"

    await interaction.followup.send(f"This is how many messages with phrase {phrase} I found: {counter}")

    #deleteMessages(messages)

#def deleteMessages(deletelist: array):
    



client.run(key, log_handler=handler)