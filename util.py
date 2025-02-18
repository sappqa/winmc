import subprocess
from config import *

class WinddcutilError(Exception):
    pass

def get_monitors():
    res = subprocess.run([WINDDCUTIL, "detect"], capture_output=True, text=True)
    if res.stderr != "":
        raise WinddcutilError(res.stderr)
    substrs = res.stdout.split('\n')
    if substrs[-1] == '':
        substrs.pop()
    monitors = []
    for s in substrs:
        monitors.append(s.split(' ')[0])
    return monitors

def issue_command_to_monitors(monitors, command):
    for monitor in monitors:
        command[2] = monitor
        res = subprocess.run(command, capture_output=True, text=True)