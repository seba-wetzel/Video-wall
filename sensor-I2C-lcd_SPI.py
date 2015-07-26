#!/usr/bin/python
import os
import sys
from subprocess import *
import time as delay
import pygame
from pygame.locals import *
import smbus
import RPi.GPIO as GPIO

#manejo de la pantalla lcd
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI 
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Raspberry Pi SPI por hardware:
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0

# disp = adafruit lcd x SPI configuracion (hardware):
disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))



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
          pantalla_lcd("valor",2,0)
          pantalla_lcd( valor,10,0)
          return valor
          sensar = False


def conDef():
   
    global interrupcion, lista , valoresMinMax, valores
    del lista[0:]
    del valoresMinMax[0:]
    for i in range(15):
        lista.append(leerSensor())
        print i
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

#comandos de la pantalla lcd
disp.begin(contrast=60)   #iniciamos la pantalla y seteamos el contraster
disp.clear()
disp.display()


def pantalla_lcd(caracteres,posX, posY):                               #generar la imagen para pasar al lcd
    image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
    texto = str(caracteres)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((posX, posY), texto, font=font)
    disp.image(image)
    disp.display()


obtenerValores()                                  #iniciamos la funcion que lee el archivo con los valores de luz
pygame.init()                                     #iniciamos pygame, sino no anda..
#fondoNike()                                       #cargamos la imagen de fondo estatica

try:
    
    while True:                                    #void loop a lo arduino
          if interrupcion:                         #mientas la variable interrupcion sea falsa esto no anda, pero cuando se activa la interrupcion, esta pasa a ser verdaero y se activa la funcion de obtener nuevos valores
                conDef()
          waitToDark = True                           #esperar a que sea oscuro True, para que sea lo primero que haga 
          waitToLight = False                         #esperar a que halla luz False, para que sea lo segundo que haga
       
          while waitToDark:
             print "wait to dark stament"
             if interrupcion:                         #mientas la variable interrupcion sea falsa esto no anda, pero cuando se activa la interrupcion, esta pasa a ser verdaero y se activa la funcion de obtener nuevos valores
                conDef()
             sensor = leerSensor()
             umbralInferior = int(minimo) +50
             if sensor < umbralInferior:
                waitToDark = False
                waitToLight = True
             else:
                  delay.sleep(0.5)
          while waitToLight :
                if interrupcion:                         #mientas la variable interrupcion sea falsa esto no anda, pero cuando se activa la interrupcion
                   conDef()
                print "wait to light stament"
                sensor = leerSensor()
               
                umbralSuperior = int(maximo) -50
                
                if sensor > umbralSuperior :
                   contador = contador+1
                   print "contador = " + str(contador)
                   delay.sleep(0.5)
                   if contador >= 3:
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
