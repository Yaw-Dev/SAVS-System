import os
import json
import state
import psutil
import win32gui
import keyboard
import win32process

def foreground_task_name():
    hwnd = win32gui.GetForegroundWindow()
    if not hwnd:
        return None
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    try:
        return psutil.Process(pid).name()
    except psutil.Error:
        return None

def command_open():
    with open('config.json', 'r') as f:
        config = json.load(f)
    application_name = config['application_names'].get(state.recognised_audio.replace('open ', ''), '')
    if "/" in application_name or "\\" in application_name:
        os.startfile(application_name)
    else:
        os.system(f"start {application_name}")

def command_exit():
    os.system("msg * SR engine stopped!")
    os._exit(0)

def command_clear_temp():
    os.system(r"start C:/Users/Nikos/Documents/clean.bat")

def command_kill_foreground():
    app_name = foreground_task_name()
    if app_name:
        os.system(f"taskkill /f /im {app_name}")

def command_start_typing():
    keyboard.write(state.recognised_audio.replace("type ", ""))

# command-function mapping
command_names = {
    "type": command_start_typing,
    "open": command_open,
    "exit engine": command_exit,
    "clear temp": command_clear_temp,
    "kill foreground": command_kill_foreground,
    "press enter": lambda: keyboard.press_and_release('enter'),
}