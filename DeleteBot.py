import array
from code import interact
import discord
from discord.ext import commands
from discord import DeletedReferencedMessage, app_commands, guild
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



class Buttons(discord.ui.View):
    def __init__(self, messages, *, timeout=180):
        super().__init__(timeout=timeout)
        self.messages = messages

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.danger)
    async def yes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Message Deleted!")
        await deleteMessages(self.messages)
    @discord.ui.button(label="No",style=discord.ButtonStyle.green)
    async def no_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        await interaction.response.edit_message(content=f"Deletion Canceled!")


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

@client.tree.command(name="delete_messages", description="Find and delete messages", guild=GUILD_ID)
async def findMessages(interaction: discord.Interaction, phrase: str, amount: int):
    await interaction.response.defer()  # Defer the response to avoid timeout

    counter = 0

    if amount < 0 or amount >= 5000:
        await interaction.followup.send(f"Please limit the search radius from 0-5000")#avoid to many messages taking to long.
        return
    channel = interaction.channel
    user_id = interaction.user.id
    messages = []
    async for message in channel.history(limit=amount):
        if message.author.id == user_id and phrase in message.content:
            messages.append(message)
            counter += 1  # Count messages with phrases.
     #counts messages with phrases.
    if len(messages) == 0:
        await interaction.followup.send(f"Please expand search radius")
        return
    prevphrase = phrase
    if phrase in badWords: #would like to have used a pointer here to be able to reference the location of it so i dont have to change phrase
        phrase = "REDACTED"

    await interaction.followup.send(f"This is how many messages with phrase '{phrase}' I found: {counter}", view=Buttons(messages))

    phrase = prevphrase #return the phrase back to its original value to make sure we can use it later if needed



async def deleteMessages(deletelist: array):
    for message in deletelist:
        await message.delete()


client.run(key, log_handler=handler)