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
disp.begin(contrast=60)   #iniciamos la pantalla y seteamos el contraster
disp.clear()
disp.display()


image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
draw = ImageDraw.Draw(image)   


def write(caracteres,posX, posY):                               #generar la imagen para pasar al lcd
    global image, draw    
    texto = str(caracteres)
    draw = ImageDraw.Draw(image)   
    font = ImageFont.load_default()
    draw.rectangle((posX,posY,posX+20,posY+10), outline=255, fill=255)
    draw.text((posX, posY), texto, font=font)
    disp.image(image)
    disp.display()

def clean ():
    disp.clear()
def blank():
    draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
