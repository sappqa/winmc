# winmc

`winmc` is a command line tool build around [winddcutil](https://github.com/rtrbt/winddcutil/) to provide easy and simultaneous control over multiple displays.

## Purpose

Most developers who work from home likely have a work laptop as well as a PC and more than one monitor. KVM switches are one way to easily switch monitor inputs between a PC and laptop, but affordable options typically have issues with higher resolutions and refresh-rates.

Assuming a setup with two monitors, a PC, and a work laptop, here is one potential solution:
- Laptop -> USB hub with two HDMI inputs -> connect to HDMI1 input on both monitors
- PC -> connect to DisplayPort input on both monitors
- Mouse, keyboard, etc. -> USB switch -> connects to both the PC and the dual-HDMI USB hub

The issue with this setup is that in order to switch your monitor inputs, you'll need to manually use the buttons on the back of both of your monitors every single time.. *yes, first-world problems, I know* 😂

You can use [winddcutil](https://github.com/rtrbt/winddcutil/) to switch your monitor inputs, but you'll need to use two separate commands. *So then why don't you just use a .bat script?* Well, originally I did and it works to switch from my laptop to my PC, but unfortunately my dual-HDMI USB hub doesn't support DDC/CI, so it isn't possible to switch back.


## How it Works

In order to get around the issue of having a dual-HDMI USB hub that doesn't support DDC/CI, `winmc` runs a TCP server on the PC-side which listens for a message from the laptop (client) and executes the monitor input switch or any other request.

## Setup

### On all devices

- Install python 3.12
- Install [winddcutil](https://github.com/rtrbt/winddcutil/)

    ```
    mkdir c:/executables/winddcutil && cd c:/executables/winddcutil
    curl -Lo winddcutil.exe https://github.com/rtrbt/winddcutil/releases/download/v0.1.0/winddcutil.x64.exe
    ```
- Install `winmc`

    ```
    git clone https://github.com/sappqa/winmc
    ```
- Create an alias for `winmc` in your `.bashrc` file

    ```
    alias mc='python C:\\path\\to\\winmc\\winmc.py'
    ```

- Code setup for `winmc`
    ```
    cd c:/path/to/winmc/
    cp config.template.py config.py
    ```
    - Set your physical monitor input channels in `config.py`
    - Set the hostnames in `config.py` to the hostnames of your devices
    - Set 'HOST' in `config.py` to the ip address of your server device
    - Set 'PORT' in `config.py` to the desired port you want to listen on. (this part is optional since the default value 65432 will work as long as it isn't already taken)
- Set up a virtual environment and install the required packages
    ```
    python -m venv .venv
    source .venv/scripts/activate
    pip install -r requirements.txt
    ```


### On the server device
- Create an inbound rule in windows defender firewall to allow listening on your desired port in `config.py`
    - Optionally, restrict access to only ip addresses of recognized devices on your LAN. For example, your client device
- Install the server executable
    ```
    mkdir c:/executables/winmc && cd c:/executables/winmc
    curl -LO https://github.com/sappqa/winmc/releases/download/v1.0.0/winmc-server.exe
    ```
    - Or you can optionally build it yourself using the following command
        ```
        pyinstaller --onefile server.py --name winmc-server --icon winmc-icon.ico
        ```
- Set `winmc-server.exe` as a windows start-up application.
    - Right click on `winmc-server.exe` > Create Shortcut
    - Open the Windows Run application using the shortcut: `Win+R`
    - Enter `shell:startup` , this should open a file explorer in the Startup apps directory
    - Move the shortcut into that directory
