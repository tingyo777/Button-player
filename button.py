import RPi.GPIO as GPIO
import wiringpi
import json
import pygame
import time
from gpiozero import Button
from signal import pause
enterdebug = "!"
startgame = "@"
setupdevice = "#"
setactivation = "^"
checkin = "%"
delimiter = '-'
button = Button(27)
LED_PIN = 17
pygame.mixer.init(22050, -16, 1, 4096)

def button_pressed():
    print("Button was pressed")
    pygame.mixer.music.load("001.mp3")
    pygame.mixer.music.play()
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(1)

def button_held():
    print("Button was held")
    #pygame.mixer.music.load("001.mp3")
    #pygame.mixer.music.play()

def button_released():
    print("Button was released")
    pygame.mixer.music.stop()
    GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(1)
def createserial():
    wiringpi.wiringPiSetup()
    serial = wiringpi.serialOpen('/dev/ttyS0', 19200)

    return serial

def closeserial(serial):
    wiringpi.serialFlush(serial)
    wiringpi.serialClose(serial)

def tx(serial, command):
    wiringpi.serialPuts(serial, command)

def setupDevice():
    serial = createserial()
    wiringpi.serialPuts(serial, setupdevice)
    wiringpi.serialPuts(serial, delimiter)

    deviceID = 0

    while wiringpi.serialDataAvail(serial):
        deviceID = wiringpi.serialGetchar(serial)

    closeserial(serial)

    return {"deviceID": deviceID}

def enterDebug():
    serial = createserial()
    wiringpi.serialPuts(serial, enterdebug)
    wiringpi.serialPuts(serial, delimiter)
    wiringpi.delay(500)

    while wiringpi.serialDataAvail(serial):
        response = wiringpi.serialGetchar(serial)
        if chr(response) == delimiter:
            deviceID = wiringpi.serialGetchar(serial)
            closeserial(serial)
            return deviceID
        else:
            continue

def startGame():
    serial = createserial()
    wiringpi.serialPuts(serial, startgame)
    wiringpi.serialPuts(serial, delimiter)
    closeserial(serial)

def setActivationDelay(numberMillis):
    serial = createserial()
    wiringpi.serialPuts(serial, setactivation)
    wiringpi.serialPuts(serial, delimiter)
    wiringpi.serialPuts(serial, numberMillis)
    closeserial(serial)

def checkInDevice():
    serial = createserial()
    wiringpi.serialPuts(serial, checkin)
    wiringpi.serialPuts(serial, delimiter)
    wiringpi.delay(500)
    field = 0
    deviceId = 0
    userWinPoints = 0
    userLosePoints = 0
    is_hunter = 0

    while wiringpi.serialDataAvail(serial):
        nextChar = wiringpi.serialGetchar(serial)
        if chr(nextChar) == delimiter:
            field += 1
            continue

        if field == 0:
            deviceId = nextChar
        if field == 1:
            userWinPoints = nextChar
        if field == 2:
            userLosePoints = nextChar
        if field == 3:
            is_hunter = nextChar

    closeserial(serial)
    return json.dumps({"deviceID": deviceId, "wins": userWinPoints, "losses": userLosePoints, "is_hunter": is_hunter})


def rx(serial):
    if wiringpi.serialDataAvail(serial):
        char = wiringpi.serialGetchar(serial)
        if char != -1:
            return char
        else:
            return None
    else:
        return None
    
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
while True:
    
    
    button.when_pressed = button_pressed
    button.when_held = button_held
    button.when_released = button_released
GPIO.cleanup()



button.when_pressed = button_pressed
button.when_held = button_held
button.when_released = button_released

pause()
