#!/usr/bin/python
import os
import sys
from subprocess import *
import RPi.GPIO as puerto
import time as delay
import pygame

puerto.setmode(puerto.BCM)
puerto.setup(24, puerto.IN)
sensor = puerto.input(24)
path = "/home/pi/nike.mp4"
fondo= "/home/pi/nike.png"
estado = False 
iniciar = True
contador = 0

def blackscreen():
    pygame.display.init()
    pygame.mouse.set_visible(False)
    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    img = pygame.image.load(fondo)
    screen.blit(img , (0, 0))


def player ():
    args = ['omxplayer', path]
    reproductor = Popen(args,stdout=open(os.devnull, 'wb'), close_fds=True,stderr=PIPE)
    salida = reproductor.communicate()
    

pygame.init()

blackscreen()

try:
    
    while True:
        while iniciar:
            sensor = puerto.input(24)
            if sensor == puerto.LOW:
                estado = False
                
       
            elif sensor == puerto.HIGH:
                print "no sensando"
                estado = True
                iniciar= False
        while estado:
            sensor = puerto.input(24)
            if sensor == puerto.HIGH:
                contador = contador+1
                delay.sleep(1)
                print "marca1"
                print contador
                if contador >3:
                    estado= False
                    contador = 0
                    print "reproduciendo"
                    player()
            else:
                print "marca2"
                contador = 0
                estado = False
                iniciar= True
    
        sensor = puerto.input(24)
        if sensor == puerto.LOW:
         iniciar = True
except KeyboardInterrupt:
    puerto.cleanup()
