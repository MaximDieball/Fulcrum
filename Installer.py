import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

# Create the client instance with the specified intents
client = discord.Client(intents=intents)


# Event handler for when the bot has successfully connected to Discord
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


# Event handler for when a message is sent in a channel the bot has access to
@client.event
async def on_message(message):
    # Check if the message is sent by the bot itself to avoid infinite loops
    if message.author == client.user:
        return

    if message.content.strip():
        # Repeat the message
        await message.channel.send(message.content)


# Run the bot with the specified token
client.run(TOKEN)