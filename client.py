
import webbrowser
import socketio
import _thread as thread
import threading
import sys


# https://pythonhosted.org/pynput/mouse.html
import pynput
from pynput.keyboard import Key, Controller as keyboardController
from pynput.mouse    import Button as mouseBtn, Controller as mouseController
from win32gui        import GetWindowText, GetForegroundWindow




# socket server URL, change to ip of your pc on your local networks
# if opted to use locally ex: http://192.168.0.1:3001 or http://localhost:3001
#
# Also, is possible to change trough CLI, add --host <socket_server_url>
# * ex: --host http://localhost:3001
# * the default url is "https://remacro.herokuapp.com"
socketURL = 'https://remacro.herokuapp.com'


# CL arguments
try:
    i = 1 # the fisrt(0) is the file
    while i < len(sys.argv):

        # --host <host>
        if(sys.argv[i] == "--host"):
            print("socket io host: " + sys.argv[i+1])
            socketURL = sys.argv[i+1]
        
        # --help / -h
        if(sys.argv[i] == '--help' or sys.argv[i] == '-h'):
            print("--host <host> | set socket.io server host")
            print("\r ex: --host http://localhost:3001")

        i+=1
    pass
except IndexError:
    print('no arguments')
    pass


sio = socketio.Client()
def tryConnect():
    sio.connect(socketURL)

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

# type some text
def ttype(text):
    keyboard = keyboardController()
    keyboard.type(str(text))

# open a url
# ! on first execution after start client.py
# ! it take a longer time to open the page
def openURL(url):
    webbrowser.open(url)




# add the button names here and use buttons[index]
# used to remote user get available buttons
# ! if is already started, need to close and start again
buttons = [
    'Alt tab',
    'open Github',
]

def keyHandler(key):
    currentWindow = GetWindowText(GetForegroundWindow())
    keyboard = keyboardController()
    mouse = mouseController()
    

    print("executing: " + key)
    if(key == buttons[0]):
        pressKeys([Key.alt, Key.tab])

    
    elif(key == buttons[1]):
        openURL("https://github.com")


    # examples

    # BASIC - copy when a 
    # if(key == "<MyButton>"):
    #     print("executing MyButton 1 : copy")
    #     pressKey([Key.ctrl, 'c'])

    # SPECIFIC WINDOW - open new tab only if chrome browser is open in foreground
    # if(currentWindow.find("Chrome>") > -1):
    #     if(key == buttons[1]):
    #         pressKeys([Key.ctrl, 'n'])
    

    # if does not match any button name
    else:
        print("invalid key/not found")
    


@sio.event
def connect():
    print("Connected")

@sio.event
def sid(user):
    print("Your ID: " + user['id'] + " @ timestamp:" + str(user['conAt']))
    print("use the id in web UI to send button press with the name")
    print("or click here: "+ socketURL + "/" + user['id'])

@sio.event
def macro(key):
    keyHandler(key['key'])

@sio.event
def getBtns(data):
    sio.emit("resBtns", {'toid': data['toid'], 'btns':buttons})
    


# this is just to start an loop and keep the script running
runner = runKeeper(1, "keep runnin")
runner.run()
