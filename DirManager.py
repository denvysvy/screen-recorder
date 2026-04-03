import sys
import os
from time import time
from tkinter import filedialog
from LogManager import log


directory = 'C:/Users/foxcv/Downloads'



video_cap = ""
audio_cap = ""

time_id = None
types = {'video': video_cap, 'audio': audio_cap}

def get_exe_dir():
    if getattr(sys, "frozen", False):
        d = os.path.dirname(sys.executable)
        log(log_type="EXE", directory=d)
        return d
    d = os.path.abspath(".")
    log(log_type="EXE", directory=d)
    return d





BASE_DIR = get_exe_dir()
WEB_DIR = os.path.join(BASE_DIR, "web")
CAPTURE_DIR = os.path.join(BASE_DIR, "capture")

screenshot_dir = os.path.join(WEB_DIR, "capture", "screenshot.png")



def debag():
    global isdebag, BASE_DIR, WEB_DIR, CAPTURE_DIR, screenshot_dir
    BASE_DIR = ""
    WEB_DIR = os.path.join(BASE_DIR, "web")
    CAPTURE_DIR = os.path.join(BASE_DIR, "capture")

    screenshot_dir = os.path.join(WEB_DIR, "capture", "screenshot.png")


def generate_time_id() -> None:
    global time_id, video_cap, audio_cap
    time_id = round(time() * 100)
    log(log_type="TIMEID", time_id=time_id)

def get_time_id() -> int | None:
    global time_id
    return time_id



def config_cap_dir() -> None:
    global video_cap, audio_cap, types
    video_cap = combine_file_with_id(r"video.avi")
    audio_cap = combine_file_with_id(r"audio.wav")
    types = {'video': video_cap, 'audio': audio_cap}
def video_cap() -> str:
    return types['video']
def audio_cap() -> str:
    return types['audio']



def correct_name(file: str) -> str:
    files = os.listdir(directory)
    file = fix_filename(file)
    name, ext = os.path.splitext(file)
    i = 1
    new_name = file
    while new_name in files:
        new_name = f"{name}({i}){ext}"
        i += 1
    return new_name
def fix_filename(file: str) -> str:
    forbidden_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    forbidden_names = [
        'CON', 'PRN', 'AUX', 'NUL',
        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    ]
    name, ext = os.path.splitext(file)
    for ch in forbidden_chars:
        name = name.replace(ch, '')
    if name.upper() in forbidden_names or name.strip() == '':
        log(level="debag", log_type="FIXNAME", name="default")
        name = "default"
    name = name.rstrip(' .')
    if not name:
        log(level="debug", log_type="FIXNAME", name="default")
        name = "default"
    return name + ext





def is_file_cap_exists(file_type: str) -> bool:
    return os.path.exists(types[file_type])

def remove_cap(file_type: str) -> None:
    log(level="debug", log_type="REMOVECAP", type=file_type, file=types[file_type])
    os.remove(types[file_type])

def combine_filename_with_dir(filename):
    return os.path.join(directory, filename)

def ask_directory():
    global directory
    directory = filedialog.askdirectory()
def get_dir():
    return directory


def combine_file_with_id(filename):
    name, ext = os.path.splitext(filename)
    filename = f"{name}{time_id}{ext}"
    return os.path.join(CAPTURE_DIR, filename)


def clean_cap():
    if is_file_cap_exists('video'): remove_cap('video')
    if is_file_cap_exists('audio'): remove_cap('audio')






if __name__ == '__main__':
    generate_time_id()
    print(combine_file_with_id(r'capture\video.avi'))
    print(f"{get_dir()}")