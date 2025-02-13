# winmc


user setup instructions
- set device hostnames in mc.py
- set ip address in server.py to the local ip of the device you want to run the server on
- choose a port to listen on with your server and set that in server.py
- set client to connect to the server device's local ip address as well as the port you chose it to listen on
- create inbound rule in windows defender firewall on your server device to allow listening on your desired port you've configured in the server program. optionally, restrict access to only ip addresses of recognized devices on your lan

on the client machine
- mkdir c:/executables/winddcutil
- download winddcutil into that directory. get it from here: https://github.com/rtrbt/winddcutil/tags
- add alias mc='C:\\dev\\repos\\winmc\\winmc.py' to your .bashrc

on the server machine
- follow the same instructions for the client machine
- run pyinstaller on server.py to generate the executable
 - pyinstaller --onefile server.py --name winmc-server --icon winmc-icon.ico
- mkdir c:/executables/winmc
- move winmc-server.exe generated from pyinstaller to c:/executables/winmc
 - (or modify pyinstaller command to send the exe file to that directory)
- set server executable as windows start-up application


usage, available commands, examples
... 