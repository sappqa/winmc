VCP_CODE_BRIGHTNESS = "16"
VCP_CODE_INPUT_SOURCE = "96"
INPUT_SOURCE_DISPLAY_PORT = "15"
INPUT_SOURCE_HDMI_1 = "17"
INPUT_SOURCE_HDMI_2 = "18"

WINDDCUTIL = "C:/executables/winddcutil/winddcutil.exe"
SERVER_EXECUTABLE_PATH = "C:/executables/winmc/winmc-server.exe"
TIMEOUT = 4


###############################################################
#                                                             #
#               Device Configuration Settings                 #
#                                                             #
###############################################################

# set these to match your physical monitor inputs
MY_PC_DISPLAY_INPUT_SOURCE = INPUT_SOURCE_DISPLAY_PORT
MY_LAPTOP_DISPLAY_INPUT_SOURCE = INPUT_SOURCE_HDMI_1

# set these to match the hostnames of your devices using the 'hostname' command
MY_PC_HOSTNAME = "your_pc's_hostname_goes_here" 
MY_LAPTOP_HOSTNAME = "your_laptop's_hostname_goes_here"

# set this to your pc's ip address. you can get this using the `ipconfig` command
HOST = "localhost"

# this is the port you will open for listening on your pc. use any port in the dynamic port range 49152 to 65535
PORT = 65432