import os
import ctypes
import discord
from dotenv import load_dotenv

FLAG_PATH = "C:\\ProgramData\\FUC Cache"

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


print(check_flags())
print(create_flag())
print(check_flags())