import os
import psutil
import win32gui
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
    os.system("start notepad.exe")

def command_exit():
    os.system("msg * SR engine stopped!")
    os._exit(0)

def command_clear_temp():
    os.system(r"start C:/Users/Nikos/Documents/clean.bat")

def command_kill_foreground():
    app_name = foreground_task_name()
    if app_name:
        os.system(f"taskkill /F /IM {app_name}")
        print(f"Killed foreground application: {app_name}")
    else:
        print("No foreground application found.")

# command-function mapping
command_names = {
    "open": command_open,
    "exit": command_exit,
    "clear temp": command_clear_temp,
    "kill foreground": command_kill_foreground
}