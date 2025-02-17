# winmc

user setup instructions

on both devices
- install python 3.12
- mkdir c:/executables/winddcutil
- download winddcutil into that directory. get it from here: https://github.com/rtrbt/winddcutil/tags
- clone the winmc repo to your desired path C:\\path\\to\\winmc\\winmc.py'
- add alias mc='python C:\\path\\to\\winmc\\winmc.py' to your .bashrc
- make a copy of config.template.py called config.py
- set your physical monitor input channels in config.py
- set the hostnames in config.py to the hostnames of your devices
- set 'HOST' in config.py to the ip address of your server device
- set 'PORT' in config.py to the desired port you want to listen on. (this part is optional since the default value 65432 will work as long as it isn't already taken)
- set up virtual environment and install packages
    ```
    python -m venv .venv
    source .venv/scripts/activate
    pip install -r requirements.txt
    ```


then, on the server machine
- create inbound rule in windows defender firewall to allow listening on your desired port in config.py. optionally, restrict access to only ip addresses of recognized devices on your lan, for example, your client device
- run pyinstaller on server.py to generate the executable
 - pyinstaller --onefile server.py --name winmc-server --icon winmc-icon.ico
- mkdir c:/executables/winmc
- move winmc-server.exe generated from pyinstaller to c:/executables/winmc
- set server executable as windows start-up application

usage, available commands, examples
todo: fill this part in