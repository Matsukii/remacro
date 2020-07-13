import pynput
import time
from datetime import datetime
import sys

# https://pythonhosted.org/pynput/mouse.html
from pynput.keyboard import Key, Controller as keyboardController
from pynput.mouse import Button as mouseBtn, Controller as mouseController
from win32gui import GetWindowText, GetForegroundWindow


# socket server 'remote' start
import subprocess
import webbrowser
import socketio

stop = True

import _thread as thread
import threading


from random import randint



startSocketServer = False

stop = True

# start socket server
if(startSocketServer):
    subprocess.Popen("node C:/Users/mathe/Desktop/macro/rmacro/rio/index.js", shell=False)
    webbrowser.open('http://localhost:3001')


sio = socketio.Client()
def tryConnect():
    sio.connect("http://localhost:3001")

try:
    tryConnect()
    webui = True
except socketio.exceptions.ConnectionError as err:
    webui = False
    pass



class runKeeper (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print("Start, keep this window open!")
        kepprun()


def kepprun():
    while stop:
        @sio.event
        def stopp(data):
            print("stopp")
            stop = False



# encapsulte keypress and type for easier use
# ONLY FOR A SINGLE KEY
def pressKey(key):
    keyboard = keyboardController()
    keyboard.press(key)
    keyboard.release(key)

# press multiple keys from an array of keys
def pressKeys(keyArr):
    keyboard = keyboardController()
    for key in keyArr:
        keyboard.press(key)

    for key in keyArr:
        keyboard.release(key)

# type some text
def type(text):
    keyboard = keyboardController()
    keyboard.type(str(text))

# open a url
# ! add uri parsing to check if is a valid url
def openURL(url):
    webbrowser.open(url)

# add the button names here and use buttons[index]
# used to remote user get available buttons
buttons = [
    'button1',
    'lol'
]

def keyHandler(key):
    keyboard = keyboardController()
    mouse = mouseController()
    
    tro = [
        'https://www.youtube.com/watch?v=0aVBvY0jIxc',
        'https://www.youtube.com/watch?v=JxmwOWxoPDk',
        'https://www.youtube.com/watch?v=L2orcrXZDoM'
    ]


    if(key == buttons[0]):
        print("executing button 1")
        pressKeys([Key.alt, Key.tab])
        # keyboard.press(Key.alt)
        # keyboard.press(Key.tab)
        # keyboard.release(Key.alt)
        # keyboard.release(Key.tab)

    
    elif(key == buttons[1]):
        # open random item from array
        openURL(tro[randint(0, len(tro)-1)])


    # example
    # if(key == "<MyButton>"):
    #     print("executing MyButton 1")
    #     pressKey(Key.alt)
    #     pressKey(Key.tab)
    
    


@sio.event
def connect():
    print("Connected")
    

@sio.event
def sid(user):
    sio.emit("mysid", user['id'])
    print("Your ID: " + user['id'] + " @ timestamp:" + str(user['conAt']))
    print("use the id in web UI to send button name")
    print("or click here: http://192.168.0.100:3001/" + user['id'])


@sio.event
def macro(key):
    print(key)
    keyHandler(key['key'])
    

@sio.event
def getBtns(data):
    sio.emit("resBtns", {'toid': data['toid'], 'btns':buttons})
    print(0)
    



runner = runKeeper(1, "keep runnin")
runner.run()
