#!/usr/bin/python
import os
import sys
from subprocess import *
import time as delay
import pygame
from pygame.locals import *
import smbus
import RPi.GPIO as GPIO
import pantalla as LCD

#todas las variables globales y constantes
bus = smbus.SMBus(1)  # La raspi rev2 usa el dev1, la raspi 2 ?
contador = 0
path = "/home/pi/nike.mp4"
fondo= "/home/pi/nike.jpg"
#listas con las configuraciones de luz
lista = []
valoresMinMax = []
interrupcion = False      #variable para la interrupcion
minimo=0
maximo=0

#leemos los valores guardados en el archivo de texto
def obtenerValores():
    global maximo, minimo
    valores = open('valores','r')
    for line in valores:
        lista.append(line.strip())
    valores.close()
    maximo = max(lista)
    minimo = min(lista)
    valoresMinMax.insert(0,minimo)
    valoresMinMax.insert(1,maximo)



def player ():
    args = ['omxplayer', path]
    reproductor = Popen(args,stdout=open(os.devnull, 'wb'), close_fds=True,stderr=PIPE)
    
    salida = reproductor.communicate()

def fondoNike():
    pygame.mouse.set_visible(False)
    img = pygame.image.load(fondo)
    ALTO = pygame.display.Info().current_w
    ANCHO = pygame.display.Info().current_h
    pygame.display.set_mode((ALTO,ANCHO),FULLSCREEN)
    pantalla  = pygame.display.get_surface()
    imgScale = pygame.transform.scale(img, (ALTO, ANCHO))
    imprimir = True
    while imprimir:
          pantalla.blit(imgScale , (0, 0))
          pygame.display.update()
          delay.sleep(0.1)
          imprimir = False

def leerSensor():
    sensar = True
    while sensar :
          data = bus.read_i2c_block_data(0x23,0x21) #0x21 corresponde a leer el sensor a 1lx de resolucion a 120ms de respuesta 
          valor = (data[1] + (256 * data[0]))       #convertimos el array de 2 bytes en un decimal
          
          return valor
          sensar = False


def conDef():
   
    global interrupcion, lista , valoresMinMax, valores
    del lista[0:]
    del valoresMinMax[0:]
    for i in range(15):
        LCD.blank()
        sensor = leerSensor()
        lista.append(sensor)
        print i
        LCD.blank()
        LCD.write('configurando',2,0)
        LCD.write( i,25,25)
        LCD.write( sensor,35,25)
        delay.sleep(0.5)
    
      
    print "fuera del def"
    maximo = max(lista)
    minimo = min(lista)
    valoresMinMax.insert(0,minimo)
    valoresMinMax.insert(1,maximo)
    valores = open('valores', 'w')
    valores.write(str (valoresMinMax[0]))
    valores.close()
    valores = open('valores', 'a')
    valores.write('\n')
    valores.write(str (valoresMinMax[1]))
    valores.close()    
    interrupcion = False
    


def activar(algo):
    global interrupcion
    interrupcion = True
    print "INTERRUPCION"
    
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(18, GPIO.RISING, callback=activar, bouncetime=1000)


obtenerValores()                                  #iniciamos la funcion que lee el archivo con los valores de luz
pygame.init()                                     #iniciamos pygame, sino no anda..
fondoNike()                                       #cargamos la imagen de fondo estatica

try:
    
    while True:
          LCD.blank()                                    #void loop a lo arduino
          if interrupcion:                         #mientas la variable interrupcion sea falsa esto no anda, pero cuando se activa la interrupcion,  se activa la funcion de obtener nuevos valores
                conDef()
          waitToDark = True                           #esperar a que sea oscuro True, para que sea lo primero que haga 
          waitToLight = False                         #esperar a que halla luz False, para que sea lo segundo que haga
       
          while waitToDark:
             print "wait to dark stament"
             LCD.write('claridad',2,0)
             
             if interrupcion:                         #mientas la variable interrupcion sea falsa esto no anda, pero cuando se activa la interrupcion,  y se activa la funcion de obtener nuevos valores
                conDef()
             sensor = leerSensor()
             LCD.write( sensor,25,25)
             umbralInferior = int(minimo) +60
             if sensor < umbralInferior:
                waitToDark = False
                waitToLight = True
             else:
                  delay.sleep(0.5)
                  
          while waitToLight :
                if interrupcion:                         #mientas la variable interrupcion sea falsa esto no anda, pero cuando se activa la interrupcion
                   conDef()
                print "wait to light stament"
                LCD.blank()
                LCD.write('oscuridad',2,0)
                sensor = leerSensor()
                LCD.write( sensor,25,25)
                umbralSuperior = int(maximo) -20
                
                if sensor > umbralSuperior :
                   contador = contador+1
                   print "contador = " + str(contador)
                   LCD.blank()
                   LCD.write("Play en ",5,10)
                   LCD.write(abs(contador-3),5,25)
                   delay.sleep(0.5)
                   if contador >= 3:
                      print "reproducir"
                      LCD.blank()
                      LCD.write("Reproduciendo",5,10)
                      player()
                      waitToLight = False
                      contador = 0
                      LCD.blank()  
                                  
                else :
                     delay.sleep(0.5)
                     #print "entro en el else"
                     contador = 0
except KeyboardInterrupt:
       print "Saliendo"
