
import webbrowser
import socketio
import _thread as thread
import threading
import sys
import subprocess
import json


# https://pythonhosted.org/pynput/mouse.html
import pynput
from pynput.keyboard import Key, KeyCode as keyCode, Controller as keyboardController
from pynput.mouse    import Button as mouseBtn, Controller as mouseController
from win32gui        import GetWindowText, GetForegroundWindow







options = {
    # socket server URL, change to ip of your pc on your local networks
    # if opted to use locally ex: http://192.168.0.1:3001 or http://localhost:3001
    #
    # Also, is possible to change trough CLI, add --host <socket_server_url>
    # * ex: --host http://localhost:3001
    # * the default url is "https://remacro.herokuapp.com"
    # "socketURL": 'https://remacro.herokuapp.com',
    "socketURL": 'https://remacro.herokuapp.com',

    # enable default actions for any application
    "enabledefault": True,

    # use profiles provided in a json file
    # set the path to the file or keep it as False
    # * ex: "C:/path/to/my-profiles.json"
    # --usekeyfile "C:/path/to/my-profiles.json"
    "usekeyfile": False,
}

# CL arguments
try:
    i = 1 # the fisrt(0) is the file
    while i < len(sys.argv):

        # --host <host>
        if(sys.argv[i] == "--host"):
            print("[ARGV] socket io host: " + sys.argv[i+1])
            socketURL = sys.argv[i+1]
        
        # --enabledefault
        if(sys.argv[i] == "--enabledefault"):
            print("[ARGV] [FLAG] default actions enabled")
            socketURL = sys.argv[i+1]
        
        # --usekeyfile
        if(sys.argv[i] == "--usekeyfile"):
            if(sys.argv[i+1] == "true"):
                options["usekeyfile"] = "profiles.json"
                print("[ARGV] [FLAG] using profiles from json, path: " + sys.argv[i+1])
            elif(sys.argv[i+1].startswith('-') == False):
                options["usekeyfile"] = sys.argv[i+1]
                print("[ARGV] [VALUE] using profiles from json, path: " + sys.argv[i+1])
                

        # --help / -h
        if(sys.argv[i] == '--help' or sys.argv[i] == '-h'):
            print("--help or -h | show this help and stop the script")
            print("--enabledefault | enable default actions for any application")
            print("--host <host> | set socket.io server host")
            print("\t ex: --host http://localhost:3001")
            print("--usekeyfile <true|file> | use profiles from json file")
            print("\n\t MOUSECLICK AND MOUSEMULTICLICKS IS NOT SUPPORTED WITH A FILE \n")
            print("\t enable with file on client.py folder with profiles.json name")
            print("\t ex: --usekeyfile true")
            print("\t enable with file with a custom path")
            print('\t ex: --usekeyfile "C:/path/to/my/profiles.json"')
            exit()

        i+=1
    pass
except IndexError:
    print('[ERR] no arguments')
    pass


# SET your keys and profiles here, following the template.json
# 
profiles = {
    "DEFAULT": {
        "name": "ACTIONS_DEFAULT",
        "windowName": "",
        "enable": options["enabledefault"],
        "desc": "if no app is available and is enable, these actions will be executed",
        "A7": {
            "name": "New tab",
            "type": "pressKeys",
            "data": [
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
        
        "A9": {
            "name": "open github",
            "type": "openURL",
            "data": "https://github.com"
        },
    },    
}



if(options["usekeyfile"] != False):
    try:
        print(options["usekeyfile"])
        keysFile = open(options["usekeyfile"], 'r')
        profiles = json.load(keysFile)
        keysFile.close()
        print("[LOAD] profiles loaded from json")
        pass
    except FileNotFoundError as identifier:
        print("[ERR] profiles file not founded, using profiles from client.py")
        pass




sio = socketio.Client()
def tryConnect():
    sio.connect(options["socketURL"])

try:
    tryConnect()
except socketio.exceptions.ConnectionError as err:
    print(err)
    pass


stop = True
class runKeeper (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print("Started, keep this window open!")
        kepprun()

def kepprun():
    while stop:
        @sio.event
        def stopp(data):
            print("stopp")
            stop = False

# get profile window names
def getWindowNames(profiles):
    names = []

    for i in profiles.keys():
        if(i != "test" and i != "template" and i != "DEFAULT"):
            names.append({
                "window": profiles[i]["windowName"],
                "profile": i
            })

    return names


# set window names on a variable
windowNames = getWindowNames(profiles)

keyboard = keyboardController()
mouse = mouseController()

# encapsulte keypress and type for easier use
# press and release a single key
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

# [Integer key codes] press multiple keys from an array of keys
def pressKeyCodes(keyArr):
    global keyboard
    for key in keyArr:
        keyboard.press(keyCode(key["keyCode"]))

    for key in keyArr:
        keyboard.release(keyCode(key["keyCode"]))


# type some text
def ttype(text):
    keyboard = keyboardController()
    keyboard.type(str(text))

# open a url
# ! on first execution after start client.py
# ! it take a longer time to open the page
def openURL(url):
    webbrowser.open(url)

# set X and Y postions of the cursor
def mouseSetPosition(coords):
    global mouse
    mouse.position = (int(coords[0]), int(coords[1]))

# move relative to current postion
def mouseMove(coords):
    global mouse
    mouse.move(int(coords[0]), int(coords[1]))

# press all mouse buttons on array and then release
def mouseMultiClicks(buttons):
    for btn in buttons:
        mouse.press(btn)

    for btn in buttons:
        mouse.release(btn)

# simple click with count
def mouseClick(button):
    global mouse
    mouse.click(button.button, button.times)

# dict of action types
actionTypes = {
    "pressKey": pressKey,
    "pressKeys": pressKeys,
    "pressKeyCodes": pressKeyCodes,
    "typeText": ttype,
    "openURL": webbrowser.open,
    "runCommand":subprocess.Popen,
    "mouseMove": mouseMove,
    "mouseSetPosition": mouseSetPosition,
    "mouseMultiClicks": mouseMultiClicks,
    "mouseClick": mouseClick,
}



def keyHandler(key):
    global profiles
    global windowNames

    def execute(key):
        currWindow = GetWindowText(GetForegroundWindow())

        profile = "DEFAULT"
        for i in windowNames:
            if(currWindow.find(i["window"]) > -1):
                profile = i["profile"]
                break
        

        profile = profiles[profile]
        if(key in profile.keys()):
            action  = profile[key]

            if(profile["enable"]):
                actionTypes[action["type"]](action["data"])
                print("[BACT] " + key + "/" + currWindow + ": " + action["name"])
            else:
                print("[INFO] actions of '" + profile["name"] + "' are disabled")



    if("button" in key):
        # print("executing: " + key["button"])
        # print(str(key["button"]))
        execute(key["button"])

    else:
        print("[ERR] key not found")
    
    



@sio.event
def connect():
    print("Connected")


@sio.event
def sid(user):
    global options
    options["userID"] = user["id"]
    print("Your ID: " + user['id'] + " | connected@timestamp: " + str(user['conAt']))
    print("use the id in web UI to send button press with the name")
    print("or click here: "+ options["socketURL"] + "/" + user['id'])

@sio.event
def macro(key):
    keyHandler(key)

@sio.event
def getBtns(data):
    sio.emit("resBtns", {'toid': data['toid'], 'profiles':str(profiles)})
    


# this is just to start an loop and keep the script running
runner = runKeeper(1, "keep runnin")
runner.run()
