import sys
import subprocess
import client
import traceback
import os
from config import *

USAGE_EXAMPLES = ["mc -h", "mc -s", "mc --switch", "mc switch", "mc -b <value> (0 ≤ value ≤ 100)"]
HELP_USAGE = ["-h", "--help"]
HELP_USAGE_DESCRIPTION = "outputs usage information"
SWITCH_USAGE = ["-s", "--switch", "switch"]
SWITCH_USAGE_DESCRIPTION = "switches monitor input channels from the pc's inputs to the laptop's inputs, or vice versa based on the current input"
BRIGHTNESS_USAGE = ["-b", "--brightness"]
BRIGHTNESS_USAGE_DESCRIPTION = "sets all monitors brightness to the value passed in. ex:  mc -b <value> (0 ≤ value ≤ 100)"
QUERY_SERVER_USAGE = ["-qs", "--query-server"]
QUERY_SERVER_USAGE_DESCRIPTION = "pings the server to see if it is active. the server will return its main thread's pid on success."
START_SERVER_USAGE = ["-ss", "--start-server"]
START_SERVER_USAGE_DESCRIPTION = "runs the server if it isn't already."
KILL_SERVER_USAGE = ["-ks", "--kill-server"]
KILL_SERVER_USAGE_DESCRIPTION = "terminates the server"

USAGES = [HELP_USAGE, SWITCH_USAGE, BRIGHTNESS_USAGE, QUERY_SERVER_USAGE, START_SERVER_USAGE, KILL_SERVER_USAGE]
USAGES_FLATTENED = sum(USAGES, [])
USAGE_DESCRIPTIONS = [HELP_USAGE_DESCRIPTION, SWITCH_USAGE_DESCRIPTION, BRIGHTNESS_USAGE_DESCRIPTION, QUERY_SERVER_USAGE_DESCRIPTION, START_SERVER_USAGE_DESCRIPTION, KILL_SERVER_USAGE_DESCRIPTION]


class UsageError(Exception):
    pass

class WinddcutilError(Exception):
    pass


def get_usage_hint():
    hint = "usage: mc [option]\n\n"
    hint += "options:\n" 
    for i in range(len(USAGES)):
        hint += f"{str(USAGES[i]):40}" + "\t" + str(USAGE_DESCRIPTIONS[i]) + "\n"
    hint += "\nexamples:\n"
    for example in USAGE_EXAMPLES:
        hint += "\t" + example + "\n"
    hint += "\n"
    return hint

def print_usage():
    print(get_usage_hint())

def get_usage_error_message():
    return f"\ninvalid usage: '{" ".join(sys.argv)}'\n\n" + get_usage_hint()

def verify_switch_usage(usage):
    for ustr in SWITCH_USAGE:
        if usage == ustr:
            return
    raise UsageError()

def verify_brightness_usage(argv1, argv2):
    flag_verified = False
    for ustr in BRIGHTNESS_USAGE:
        if argv1 == ustr:
            flag_verified = True
    if flag_verified:
        if int(argv2) >= 0 and int(argv2) <= 100:
            return
    raise UsageError()

def verify_usage():
    argc = len(sys.argv)
    if argc < 2 or argc > 3:
        raise UsageError()
    
    if sys.argv[1] in USAGES_FLATTENED:
        if argc == 2 and sys.argv[1] in BRIGHTNESS_USAGE:
            raise UsageError()
        elif argc == 3 and sys.argv[1] in BRIGHTNESS_USAGE:
            verify_brightness_usage(sys.argv[1], sys.argv[2])
    else:
        raise UsageError()
        

def get_device_hostname():
    return subprocess.run(["hostname"], capture_output=True, text=True).stdout.removesuffix('\n')
    
def verify_monitors():
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


def switch_monitor_inputs(hostname, monitors):
    # available input sources can be obtained from the 'capabilities' command ex: 60(11 12 0F)
    # 0x0F - display port
    # 0x11 - hdmi 1
    # 0x12 - hdmi 2
    # see reference, page 81: https://milek7.pl/ddcbacklight/mccs.pdf
    if hostname == MY_PC_HOSTNAME:
        print("attempting to switch monitor inputs from pc to laptop...")
        for monitor in monitors:
            res = subprocess.run([WINDDCUTIL, "setvcp", monitor, VCP_CODE_INPUT_SOURCE, MY_LAPTOP_DISPLAY_INPUT_SOURCE], capture_output=True, text=True)
            if res.stderr == "":
                print(f"successfully set input for monitor {monitor}")
            else:
                print(f"failed to set monitor {monitor} input:\n{res.stderr}")
    elif hostname == MY_LAPTOP_HOSTNAME:
        print("attempting to switch monitor inputs from laptop to pc...")
        if client.send_request(SWITCH_USAGE[0]):
            for monitor in monitors:
                res = subprocess.run([WINDDCUTIL, "setvcp", monitor, VCP_CODE_INPUT_SOURCE, MY_PC_DISPLAY_INPUT_SOURCE], capture_output=True, text=True)
                if res.stderr == "":
                    print(f"successfully set input for monitor {monitor}")
                else:
                    print(f"failed to set monitor {monitor} input:\n{res.stderr}")
    else:
        print(f"unknown device hostname: {hostname}")

def adjust_monitor_brightness(monitors, brightness):
    for monitor in monitors:
        res = subprocess.run([WINDDCUTIL, "setvcp", monitor, VCP_CODE_BRIGHTNESS, brightness], capture_output=True, text=True)
        if res.stderr == "":
            print(f"successfully set brightness for monitor {monitor}")
        else:
            print(f"failed to set monitor {monitor} brightness:\n{res.stderr}")

def start_server():
    if os.path.exists(SERVER_EXECUTABLE_PATH):
        data = client.send_request(QUERY_SERVER_USAGE[0], suppress=True)
        if data is None:
            subprocess.Popen([SERVER_EXECUTABLE_PATH], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
            print("successfully started server")
        else:
            print("server already running")
    else:
        print("unable to start server, executable not found")
        
def exec():
    argc = len(sys.argv)
    monitors = verify_monitors()
    if sys.argv[1] in HELP_USAGE:
        print_usage()
    elif sys.argv[1] in SWITCH_USAGE:
        hostname = get_device_hostname()
        switch_monitor_inputs(hostname, monitors)
    elif sys.argv[1] in BRIGHTNESS_USAGE:
        adjust_monitor_brightness(monitors, sys.argv[2])
    elif sys.argv[1] in QUERY_SERVER_USAGE:
        data = client.send_request(QUERY_SERVER_USAGE[0])
        if data is not None:
            print(f"query successful, server pid: {str(data.decode())}")
    elif sys.argv[1] in START_SERVER_USAGE:
        start_server()
    elif sys.argv[1] in KILL_SERVER_USAGE:
        data = client.send_request(KILL_SERVER_USAGE[0])
        if data is not None:
            print("server terminated")


try:
    verify_usage()
    exec()
except UsageError:
    print(get_usage_error_message())
    traceback.print_exc()
except WinddcutilError as wde:
    print(str(wde))
    traceback.print_exc()
except ValueError as ve:
    if "invalid literal for int()" in str(ve):
        print(get_usage_error_message())
    else:
        print(ve)
    traceback.print_exc()
except Exception as ex:
    print("unknown exception occurred: " + str(ex))
    traceback.print_exc()
