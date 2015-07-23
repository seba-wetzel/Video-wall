#!/usr/bin/python
import os
import sys
from subprocess import *

import time as delay
import pygame
from pygame.locals import *
import smbus

bus = smbus.SMBus(1)  # La raspi rev2 usa el dev1, la raspi 2 ?
direccion = 0x23 # address del sensor i2c cuando el pin adr esta a LOW
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
    

#def convertToInt(data) :   #funcion para covertir los 2 bytes de respuesta en un entero
    #print ((data[1] + (256 * data[0])) / 1.2)
    #return ((data[1] + (256 * data[0])) / 1.2)

def leerSensor(addr=direccion):
    sensar = True
    while sensar :
          data = bus.read_i2c_block_data(0x23,0x21) #0x21 corresponde a leer el sensor a 1lx de resolucion a 120ms de respuesta 
          valor = (data[1] + (256 * data[0]))   
          return valor
          sensar = False


pygame.init()
fondoNike()

try:
    
    while True:
        while iniciar:
            sensor = leerSensor()
            if sensor <= 50:
                estado = False
                
       
            elif sensor >= 50:
                estado = True
                iniciar= False
        while estado:
            sensor = leerSensor()
            if sensor >=50:
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
    
        sensor = leerSensor()
        if sensor <= 50:
         iniciar = True
except KeyboardInterrupt:
       print "Saliendo"
