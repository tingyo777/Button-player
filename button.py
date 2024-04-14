import RPi.GPIO as GPIO
import pygame
import time
from gpiozero import Button
from signal import pause
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