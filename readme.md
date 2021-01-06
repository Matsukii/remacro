# remacro
Remote macro keys trough websockets

[Online Remote control page](https://remacro.herokuapp.com)

Send keyboard and mouse input trough socket.io to a python client from internet or on your local network

you can use either locally, by cloning and install node dependencies or trough the the web on rs-macro.herokuapp.com.


## Why?

Sometimes you need to send a combination of keys, but can't reach the keyboard and have you phone next, or maybe need to send keystrokes to control a devicxe without the keyboard, well, there it is

This is part of the [sMacros](https://github.com/Matsukii/sMacros), the idea came from it with socket.io integration to control other things trhoug arduino and what actually made start was when a friend was streaming and need to change scenes while is playing


### About security

_"So, can you install python and run this (not-suspicious) script and let me control the key combinations you set from internet?"_ - Ehhh..., no?

Using localy should be fine, using the socket server online may have security issues, however, the host uses https, the generated id on client **is not** saved to any database/file (code availabe at ['rio' branch](https://github.com/Matsukii/remacro/tree/rio) or rio folder) and when the client reconnect the code changes



## Usage

For both options is required to have python (3.7+ recommended) and pip to install dependencies (pynput, thread, socketio...) <br>
For local socket.io server is required to have node.js and npm setted up

download and open client.py with a text editor, create your own key events or use a profile.json file as detailed further


## Options

all can be set from command line

use -h or --help to view all comnands (the script will not be executed entirely)

tip: create a shortcut to the client.py, and change the destiny with options to execute with python in a dlouble click or open with

```py

options = {
    # socket server URL, change to ip of your pc on your local networks
    # if opted to use locally ex: http://192.168.0.1:3001 or http://localhost:3001
    #
    # Also, is possible to change trough CLI, add --host <socket_server_url>
    # * ex: --host http://localhost:3001
    # * the default url is "https://remacro.herokuapp.com"
    # "socketURL": 'https://remacro.herokuapp.com',
    "socketURL": 'http://localhost:3001',

    # enable default actions for any application
    "enabledefault": True,

    # use profiles provided in a json file
    # set the path to the file or keep it as False
    # * ex: "C:/path/to/my-profiles.json"
    # --usekeyfile "C:/path/to/my-profiles.json"
    "usekeyfile": False,
}
```

## Add profiles and buttons:

_If you want to save the profiles to a .json file, use pressKeyCodes instead of pressKeys (detailed below) and set the "useFile" on options flag to True or add --usekeyfile [<path/to/profiles.json> or true] in command line._

_*IMPORTANT: mouseClick and mouseMultiClicks is not supported with .json file*_

Key codes:

- [here is a list of keyCodes](https://gist.github.com/Matsukii/fbd15c688e39e2033d244e939b3aa7a5)
- [also try out keycode.info](https://keycode.info)

```py

# add the button name here
#
# these are the names that will be sent to web UI to create
# a list of buttons and sent back to client when a button is clicked
profiles = [
    "MYPROFILENAME": {
        "name": "custom profile",
        "windowName": "Chrome",
        "desc": "macro keys for Google Chrome",

        # True or False to enable/disable
        "enable": True,

        # buttons
        "A7": {
            "name": "New tab",
            
            # see template.json to view all types os actions as example
            "type": "pressKeys",
            
            # depend on type, for pressKeys is a array, for pressKey is only the key
            "data": [
                # Key.<your_key> to use keys like ctrl, alt, shift... 
                Key.ctrl,
                "t"
            ]
        },
        "A8": {
            "name": "Close tab",
            "type": "pressKeys",
            "data": [
                Key.ctrl,
                "w"
            ]
        },
        
        # if using json file for profiles:
        "A9": {
            "name": "Close tab",
            "type": "pressKeyCodes",
            "data": [
                {
                    "key": "ctrl",
                    "keyCode": 17,
                    "isModifier": true
                },
                {
                    "key": "w",
                    "keyCode": 87
                }
            ]
        },
        
        "B0": {
            "name": "open github",
            "type": "openURL",
            "data": "https://github.com"
        },
    },

]
```


## Encapsulated functions and some examples:
```py
# there is some functios to make easies to use,
# it just encapsulate from keyboard and mouse
# controllers
# 
# pressKey(<key>)
# pressKeys(<Array of keys to press>)
# openURL(<url>) 

# alt + tab, will press all keys in the array and then release all
pressKeys([Key.alt, Key.tab])

# press ctrl+c
pressKeys([Key.ctrl, 'c'])


# This following may NOT work, the function loops trough
# the array and press all of them then loop again releasing
# basically will should like press ctrl+c+v
pressKeys([Key.ctrl, 'c', Key.ctrl, 'v'])

# esc, will press a single key and release
pressKey(Key.esc)

# open a url in default browser,
# ! on first click after start client.py it 
# ! take a longer time to actually open
openURL("https://github.com")

# type some text
ttype("hi")

# other available types in dictionary:
actionTypes = {
    "pressKey": pressKey,
    "pressKeys": pressKeys,

    # use integer keyCode to press the keys, the profiles can be saved in a json file
    # but need a structure like the following example in "data":[] array of pressKeyCodes type:
    # ex: data: [ {"key": "ctrl", "keyCode": 17, "isModifier": true}, {"key": "t", "keyCode": 84} ] 
    "pressKeyCodes": pressKeyCodes,
    
    "typeText": ttype,
    "openURL": webbrowser.open,             # open a URL on default browser
    "runCommand":subprocess.Popen,          # run on cmd 
    "mouseMove": mouseMove,                 # relative to current position: mouseMove([X, -Y]) -> mouseMove([10, -5])
    "mouseSetPosition": mouseSetPosition,   # mouseSetPosition([X, Y])
    "mouseMultiClicks": mouseMultiClicks,   # mouseMultiClicks([mouseBtn.rigth, mouseBtn.left])
    "mouseClick": mouseClick,               # mouseClick({"button": mouseBtn.left, "times": 2}) -> a double left click
}


```

## You can find more about pynput here:
This project uses pynput, check out the [dev repository](https://github.com/moses-palmer/pynput)

- [Pynput](https://pythonhosted.org/pynput/)
- [Keyboard](https://pynput.readthedocs.io/en/latest/keyboard.html)
- [Mouse](https://pynput.readthedocs.io/en/latest/mouse.html)
- [Limitations](https://pynput.readthedocs.io/en/latest/limitations.html)


## Run

_If using devices on your network, you may need to open the port on windows firewall_

If you wnt to use locally on your network, set 'socketURL' variale to IP of the device where its running 
```ex: http://localhost:3001 or http://192.168.0.1:3001```

- Is possible to set trough command line using --host [url]
- Gonna use your phone to send click? make sure to use the local ip of host device and allow other devices to access by adding a rule with the PORT NUMBER in windows firewall


Run client.py with python(3.7+) trough cmd/shell with or without --host and keep it open <br>
_If using locally, install dependencies with `npm install` and start the server with `npm start` on `rio` folder_

After start and connect to socket.io server the ID and a url with ID will be printed

Open the url or copy the code and go to `https://remacro.herokuapp.com` _localhost:3001 on local_, paste the code and click start and you are ready to use

## Changelog
* 2020/Aug/09
    - Created and pushed 

* 2021/Jan/06
    - profiles for current window!
    - Json file load for profiles
    - better way to set keys, no need to set name and use functions manually
    - better documentation i guess
    - more actions
        - run cli commands
        - mouse click and reposition
    - "imaspeeeeed" - speed should increase a bit

<br>
<br>

# Licence: MIT


