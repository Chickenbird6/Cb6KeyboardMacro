from pymouse import PyMouse
from pykeyboard import PyKeyboard
from time import sleep
from string import printable

settingsFile = "settings.txt"
filename = "macro.txt"

actions = []

specialCharacters = ["SPACE", "ENTER", "SHIFT", "CTRL", "ALT", "ESCAPE", "DELETE", "BACKSPACE"]

macroContents = ""

# Settings variables
loggingEnabled = False
loops = 1
loopForever = False
loopDelay = 1
startDelay = 0

m = PyMouse()
k = PyKeyboard()
def get_special_key(key):
    if key == "SPACE":
        return " "
    elif key == "ENTER":
        return k.enter_key
    elif key == "CTRL":
        return k.control_key
    elif key == "ALT":
        return k.alt_key
    elif key == "ESCAPE":
        return k.escape_key
    elif key == "DELETE":
        return k.delete_key
    elif key == "BACKSPACE":
        return k.backspace_key

def check_valid_action(line):
    # split the line into readable segments
    args = line.split(" ")
    # a variable used to determine if the line is valid
    result = False

    if "#" in args[0]:
        return result

    # if the number of args is 3
    if len(args) == 3:
        # if the first arg is a valid action
        if args[0] == "key" and (args[1] in printable or args[1] in specialCharacters) and args[2] == "down" or args[2] == "up":
            result = True
        else:
            result = False

    # if the number of args is 2
    if len(args) == 2:

        if args[0] == "sleep" and float(args[1]) >= 0:
            result = True

        if args[0] == "tap" and (args[1] in printable or args[1] in specialCharacters):
            result = True

    if args[0] == "type":
        for i in range(len(args)):
            for letter in args[i]:
                if letter in printable:
                    result = True
                else:
                    result = False
                    break

    return result

def run(line):
    # split the line into readable segments
    args = line.split(" ")

    if args[0] == "key":
        if args[2] == "down":
            if args[1] in specialCharacters:
                k.press_key(get_special_key(args[1]))
            else:
                k.press_key(args[1])
        elif args[2] == "up":
            if args[1] in specialCharacters:
                k.release_key(get_special_key(args[1]))
            else:
                k.release_key(args[1])

    if args[0] == "tap":
        if args[1] not in specialCharacters:
            k.tap_key(args[1])
        else:
            k.tap_key(get_special_key(args[1]))

    if args[0] == "type":
        typeString = ""
        for i in range(1, len(args)):
            typeString += args[i] + " "
        k.type_string(typeString)

    if args[0] == "sleep":
        sleep(float(args[1]))

def run_macro(macro):
    for i in macro:
        if loggingEnabled:
            print("Logging: " + i)
        run(i)

def check_valid_macro(file):
    with open(file, 'r') as f:
        for line in f:
            # remove newlines
            line = line.replace('\n', '')
            # if the action is valid add it to the macro
            if check_valid_action(line):
                actions.append(line)

def getBoolean(string):
    if string == "True":
        return True
    return False
def check_settings(line):
    global loggingEnabled
    global loops
    global filename
    global loopForever
    global loopDelay
    global startDelay

    args = line.split("=")

    if args[0] == "loggingEnabled":
        loggingEnabled = getBoolean(args[1])

    elif args[0] == "filename":
        # set the filename to the filename in settings.txt
        filename = args[1]

    elif args[0] == "loops":
        try:
            loops = abs(int(args[1]))
        except:
            print("Expected an integer for loops")

    elif args[0] == "loopForever":
        loopForever = getBoolean(args[1])

    elif args[0] == "loopDelay":
        try:
            loopDelay = abs(int(args[1]))
        except:
            print("Expected an integer for loopDelay")

    elif args[0] == "startDelay":
        try:
            startDelay = abs(int(args[1]))
        except:
            print("Expected an integer for startDelay")
def read_settings():
    with open(settingsFile, 'r') as f:
        for line in f:
            # remove newlines
            line = line.replace('\n', '')

            check_settings(line)

read_settings()

check_valid_macro(filename)
if loggingEnabled:
    print("Logging: waiting " + str(startDelay) + " seconds to start")
sleep(startDelay)

for i in range(loops):
    run_macro(actions)
    sleep(loopDelay)

while loopForever:
    run_macro(actions)
    sleep(loopDelay)