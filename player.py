import os
import sys
import subprocess
import serial
import pygame
import time 

pygame.init()

path = "/home/pi/test.mp4"

arduino=serial.Serial('/dev/ttyACM1', 9600, timeout=1.0)
arduino.open()
inicio='p'


def blackscreen():
    pygame.display.init()
    pygame.mouse.set_visible(False)
    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
  
def player ():
    args = ['omxplayer', path]
    subprocess.Popen(args,stdout=open(os.devnull, 'wb'), close_fds=True)
   
#blackscreen()
time.sleep(1)
arduino.setDTR(False)
time.sleep(1)
arduino.flushInput()
arduino.setDTR(True)
arduino.write(inicio)
try:
    while True:
        entrada=arduino.readline()
        print entrada
        if entrada == 'R':
            player()
except KeyboardInterrupt:
    arduino.close()