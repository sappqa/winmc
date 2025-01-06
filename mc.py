import sys
import subprocess

WINDDCUTIL = "C:/executables/winddcutil/winddcutil.exe"
MY_PC_HOSTNAME = "your_pc's_hostname_goes_here"
MY_LAPTOP_HOSTNAME_1 = "your_laptop's_hostname_goes_here"
VCP_CODE_BRIGHTNESS = "16"
VCP_CODE_INPUT_SOURCE = 96
USAGE_EXAMPLES = ["mc -s", "mc --switch", "mc switch", "mc -b <value> (0 ≤ value ≤ 100)"]
SWITCH_USAGE = ["-s", "--switch", "switch"]
BRIGHTNESS_USAGE = ["-b", "--brightness"]

class UsageError(Exception):
    pass

class WinddcutilError(Exception):
    pass

def get_usage_error_message():
    message = f"invalid usage: '{sys.argv}'\n" + "here are some usage examples:\n"
    for example in USAGE_EXAMPLES:
        message += f"> {example}\n"
    return message

def verify_switch_usage(usage):
    for ustr in SWITCH_USAGE:
        if (usage == ustr):
            return
    raise UsageError()

def verify_brightness_usage(argv1, argv2):
    flag_verified = False
    for ustr in BRIGHTNESS_USAGE:
        if (argv1 == ustr):
            flag_verified = True
    if (flag_verified):
        if (int(argv2) >= 0 and int(argv2) <= 100):
            return
    raise UsageError()

def verify_usage():
    argc = len(sys.argv)
    if (argc < 2 or argc > 3):
        raise UsageError()
    elif (argc == 2):
        verify_switch_usage(sys.argv[1])
    elif (argc == 3):
        verify_brightness_usage(sys.argv[1], sys.argv[2])

def verify_device():
    hostname = subprocess.run(["hostname"], capture_output=True, text=True).stdout.removesuffix('\n')
    if (hostname == MY_PC_HOSTNAME):
        return hostname
    elif (hostname == MY_LAPTOP_HOSTNAME_1):
        return hostname
    else:
        raise ValueError(f"error: unauthorized device '{hostname}'")
    
def verify_monitors():
    res = subprocess.run([WINDDCUTIL, "detect"], capture_output=True, text=True)
    if (res.stderr != ""):
        raise WinddcutilError(res.stderr)
    substrs = res.stdout.split('\n')
    if (substrs[-1] == ''):
        substrs.pop()
    monitors = []
    for s in substrs:
        monitors.append(s.split(' ')[0])
    return monitors

def switch_monitor_inputs(hostname, monitors):
    # available input sources can be obtained from the 'capabilities' command ex: 60(11 12 0F)
    # are those values standardized? also may need to add instructions on how to make sense of those numbers
    # need to gracefully handle edge case where there isnt any other monitor input... should just do nothing or maybe print a message
    if (hostname == MY_PC_HOSTNAME):
        print("attempting to switch monitor inputs from pc to laptop...")
        for monitor in monitors:
            res = subprocess.run([WINDDCUTIL, "setvcp", monitor, VCP_CODE_INPUT_SOURCE, 15], capture_output=True, text=True)
            if (res.stderr == ""):
                print("successfully set brightness for monitor 1")
            else:
                print(f"failed to set monitor 1 brightness:\n{res.stderr}")

    elif (hostname == MY_LAPTOP_HOSTNAME_1):
        print("attempting to switch monitor inputs from laptop to pc...")
        print("sending signal to pc...")
    print("successfully switched monitor inputs")

def adjust_monitor_brightness(monitors):
    brightness = sys.argv[2]
    for monitor in monitors:
        res = subprocess.run([WINDDCUTIL, "setvcp", monitor, VCP_CODE_BRIGHTNESS, brightness], capture_output=True, text=True)
        if (res.stderr == ""):
            print("successfully set brightness for monitor 1")
        else:
            print(f"failed to set monitor 1 brightness:\n{res.stderr}")

def exec(hostname):
    argc = len(sys.argv)
    monitors = verify_monitors()
    if (argc == 2):
        switch_monitor_inputs(hostname, monitors)
    elif (argc == 3):
        adjust_monitor_brightness(monitors)


try:
    verify_usage()
    hostname = verify_device()
    print(f"hostname '{hostname}' approved. continuing...")
    exec(hostname)
    exit(0)
except UsageError:
    print(get_usage_error_message())
    exit(1)
except WinddcutilError as wde:
    print(str(wde))
    exit(1)
except ValueError as ve:
    if ("invalid literal for int()" in str(ve)):
        print(get_usage_error_message())
    else:
        print(ve)
    exit(1)
except Exception as ex:
    print("unknown exception occurred: " + str(ex))
    exit(1)
