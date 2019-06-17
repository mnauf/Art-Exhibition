#!/bin/bash
#Libraries
import RPi.GPIO as GPIO
import time
import pygame
import os

pygame.mixer.init()
pygame.mixer.music.load("qurban.mp3")
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
button = 27
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
def main():
    #GPIO.output(led, False)
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            if dist < 220:
                break
        print("I am triggered")
        #GPIO.output(led, True)
        #GPIO.input(button)==1:
        pygame.mixer.music.play()
        #input("Press button")
        while pygame.mixer.music.get_busy()==1:
            if GPIO.input(button)==0:
                pygame.mixer.music.stop()
                main()  
         #   if GPIO.input(button)==1:
          #      main()
                

 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
        #GPIO.setmode(GPIO.BCM)
        #GPIO.output(LED, False)
main()
