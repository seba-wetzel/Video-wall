#!/usr/bin/python
import os
import sys
from subprocess import *
import RPi.GPIO as puerto
import time as delay
import pygame
from pygame.locals import *

puerto.setmode(puerto.BCM)
puerto.setup(24, puerto.IN)
sensor = puerto.input(24)
path = "/home/pi/nike.mp4"
fondo= "/home/pi/nike.jpg"
estado = False 
iniciar = True
contador = 0


def fondoNike():
    pygame.mouse.set_visible(False)
    img = pygame.image.load(fondo)
    ALTO = pygame.display.Info().current_w
    ANCHO = pygame.display.Info().current_h
    pygame.display.set_mode((ALTO,ANCHO),FULLSCREEN)
    pantalla  = pygame.display.get_surface()
    imprimir = True
    while imprimir:
          pantalla.blit(img , (0, 0))
          pygame.display.update()
          delay.sleep(0.1)
          imprimir = False

def player ():
    args = ['omxplayer', path]
    reproductor = Popen(args,stdout=open(os.devnull, 'wb'), close_fds=True,stderr=PIPE)
    salida = reproductor.communicate()
    

pygame.init()
fondoNike()

try:
    
    while True:
        while iniciar:
            sensor = puerto.input(24)
            if sensor == puerto.LOW:
                estado = False
                
       
            elif sensor == puerto.HIGH:
                estado = True
                iniciar= False
        while estado:
            sensor = puerto.input(24)
            if sensor == puerto.HIGH:
                contador = contador+1
                delay.sleep(0.1)
                if contador >2:
                    estado= False
                    contador = 0
                    player()
            else:
                contador = 0
                estado = False
                iniciar= True
    
        sensor = puerto.input(24)
        if sensor == puerto.LOW:
         iniciar = True
except KeyboardInterrupt:
    puerto.cleanup()
