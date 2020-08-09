# remacro


[Online Remote control page](https://remacro.herokuapp.com)

Send keyboard and mouse input trough socket.io to a python client from internet or on your local network

you can use either locally, by cloning and install node dependencies or trough the the web on rs-macro.herokuapp.com.


## Why?

Sometimes you need to send a combination of keys, but can't reach the keyboard and have you phone next, or maybe need to send keystrokes to control a devicxe without the keyboard, well, there it is

This is part of the [sMacros](https://github.com/Matsukii/sMacros), the idea came from it with socket.io integration to control other things trhoug arduino and what actually made start was when a friend was streaming and need to change scenes while is playing


### About security

_"So, can you install python and run this (not-suspicious) script and let me control the key combinations you set from internet?"_ - Ehhh..., no?

Using localy should be fine, using the socket server online may have security issues, however, the host uses https, the generated id on client **is not** saved to any database/file (code availabe at ['rio' branch](https://github.com/Matsukii/remacro/tree/rio)) and when the client reconnect the code changes



## Usage

For both options is required to have python (3.7+ recommended) and pip to install dependencies (pynput, thread, socketio...) <br>
For local socket.io server is required to have node.js and npm setted up

download and open rMacro.py with a text editor, create your own key events


### Add buttons:

```py

# add the button name here
#
# these are the names that will be sent to web UI to create
# a list of buttons and sent back to client when a button is clicked
buttons = [
    'button1',      # index: 0
    'MyNewButton'   # index: 1
]


# then go to
def keyHandler(key):
# and add a condition using the index of the button name you want to use
# * You shoul use only one button for one action in general cases,
# * or it will execute both of your key presses when you click

def keyHandler(key):

    # when the button coming from web is equal to button in position 0 (button1),
    # will execute alt+tab
    if(key == buttons[0]):
        pressKeys([Key.alt, Key.tab])
    
    # if key name is equal to 'MyNewButton', press Windows or command(Mac) key
    elif(key == buttons[1]):
        pressKey(Key.cmd)

    else:
        print(key + "action is not defined")
```


encapsulated functions examples:

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

# basically will be like press ctrl+c+v
pressKeys([Key.ctrl, 'c', Key.ctrl, 'v'])

# esc, will press a single key and release
pressKey(Key.esc)

# open a url in default browser,
# ! on first click after start client.py it 
# ! take a longer time to actually open
openURL("https://github.com")

# type some text
ttype("hi")

```

### You can find more about pynput here:
This project uses pynput, check out the [dev repository](https://github.com/moses-palmer/pynput)

- [Pynput](https://pythonhosted.org/pynput/)
- [Keyboard](https://pynput.readthedocs.io/en/latest/keyboard.html)
- [Mouse](https://pynput.readthedocs.io/en/latest/mouse.html)
- [Limitations](https://pynput.readthedocs.io/en/latest/limitations.html)


### Run

If you wnt to use locally on your network, set 'socketURL' variale to IP of the device where its running 
```ex: http://localhost:3001 or http://192.168.0.1:3001```

- Is possible to set trough command line using --host [url]
- Gonna use your phone to send click? make sure to use the local ip of host device and allow other devices to access by adding a rule with the PORT NUMBER in windows firewall


Run client.py with python(3.7+) trough cmd/shell with or without --host and keep it open <br>
_If using locally, install dependencies with `npm install` and start the server with `npm start` on `rio` folder_

After start and connect to socket.io server the ID and a url with ID will be printed

Open the url or copy the code and go to `https://remacro.herokuapp.com` _localhost:3001 on local_, paste the code and click start and you are ready to use

