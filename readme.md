# winmc

user setup instructions

on both devices
- install python 3.12
- mkdir c:/executables/winddcutil
- download winddcutil into that directory. get it from here: https://github.com/rtrbt/winddcutil/tags
- clone the winmc repo to your desired path C:\\path\\to\\winmc\\winmc.py'
- add alias mc='python C:\\path\\to\\winmc\\winmc.py' to your .bashrc
- set the hostname in winmc.py to the hostname of your device
- set up virtual environment and install packages
    ```
    python -m venv .venv
    source .venv/scripts/activate
    pip install -r requirements.txt
    ```
- set 'HOST' in client.py to the ip address of the server

then, on the server machine
- set ip address in server.py to the local ip of the device you want to run the server on
- choose a port to listen on with your server and set that in server.py (this part is optional since the default value 65432 will work as long as it isn't taken) 
- create inbound rule in windows defender firewall to allow listening on that port. optionally, restrict access to only ip addresses of recognized devices on your lan, for example, your client device
- run pyinstaller on server.py to generate the executable
 - pyinstaller --onefile server.py --name winmc-server --icon winmc-icon.ico
- mkdir c:/executables/winmc
- move winmc-server.exe generated from pyinstaller to c:/executables/winmc
- set server executable as windows start-up application

usage, available commands, examples
todo: fill this part in