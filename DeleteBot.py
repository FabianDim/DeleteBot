import discord
import sys
import os
from dotenv import load_dotenv
from Logger import Logger

# Explicitly specify the path to the .env file
dotenv_path = 'C:\\Repos\\DeleteBot\\Key.env'
load_dotenv(dotenv_path)

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello World!')

handler = Logger.handler
key = os.getenv('DISCORD_KEY')
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(key, log_handler=handler)