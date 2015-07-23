#!/usr/bin/python
import os
import sys
from subprocess import *
import time as delay
import pygame
from pygame.locals import *
import smbus



bus = smbus.SMBus(1)  # La raspi rev2 usa el dev1, la raspi 2 ?
contador = 0
path ="home/pi/nike.mp4"

def player ():
    args = ['omxplayer', path]
    print "dentro del def player"
    reproductor = Popen(args,stdout=open(os.devnull, 'wb'), close_fds=True,stderr=PIPE)
    salida = reproductor.communicate()


def leerSensor():
    sensar = True
    while sensar :
          data = bus.read_i2c_block_data(0x23,0x21) #0x21 corresponde a leer el sensor a 1lx de resolucion a 120ms de respuesta 
          valor = (data[1] + (256 * data[0]))
          print valor
          return valor
          sensar = False

try:

    while True:
       waitToDark = True
       waitToLight = False
       
       while waitToDark:
             print "wait to dark stament"
             sensor = leerSensor()
             if sensor < 50:
                waitToDark = False
                waitToLight = True
             else:
                  delay.sleep(0.5)
       while waitToLight :
             print "wait to light stament"
             sensor = leerSensor()
             if sensor > 50 :
                contador = contador+1
                print "contador = " + str(contador)
                delay.sleep(1)
                if contador > 3:
                   print "reproducir"
                   player()
                   waitToLight = False
                   contador = 0
                                  
             else :
                  delay.sleep(0.5)
                  #print "entro en el else"
                  contador = 0
except KeyboardInterrupt:
       print "Saliendo"

