import spidev
import time
import RPi.GPIO as GPIO
import math
import Image
import ImageDraw
import time
from rgbmatrix import Adafruit_RGBmatrix

matrix = Adafruit_RGBmatrix(32, 1)


#Evan Atchison & Zayra Lobo
#December 5, 2017
#Using rpi-rgb-led-matrix-py library, draws a spectrum on a 32x32 array #given a 32 bit array of values between 0 and 31

def drawSpectrum(amp):

    # Bitmap example w/graphics prims
    image = Image.new("RGB", (32, 32))
    draw  = ImageDraw.Draw(image)   # Declare Draw instance before prims
    
    count = 0
    i = 0
    matrix.Clear()
    
#Use draw.line in library to draw the spectrum with amp values
    draw.line((0, 0, 0, amp[0]), fill = "#FF0000")
    draw.line((1, 0, 1, amp[0]), fill = "#FF0000")
    
    draw.line((2, 0, 2, amp[1]), fill = "#FF8000")
    draw.line((3, 0, 3, amp[1]), fill = "#FF8000")

    draw.line((4, 0, 4, amp[2]), fill = "#FFFF00")
    draw.line((5, 0, 5, amp[2]), fill = "#FFFF00")
    
    draw.line((6, 0, 6, amp[3]), fill = "#80FF00")
    draw.line((7, 0, 7, amp[3]), fill = "#80FF00")

    draw.line((8, 0, 8, amp[4]), fill = "#00FF00")
    draw.line((9, 0, 9, amp[4]), fill = "#00FF00")
    
    draw.line((10, 0, 10, amp[5]), fill = "#00FF80")
    draw.line((11, 0, 11, amp[5]), fill = "#00FF80")

    draw.line((12, 0, 12, amp[6]), fill = "#00FFFF")
    draw.line((13, 0, 13, amp[6]), fill = "#00FFFF")
    
    draw.line((14, 0, 14, amp[7]), fill = "#0080FF")
    draw.line((15, 0, 15, amp[7]), fill = "#0080FF")

    draw.line((16, 0, 16, amp[8]), fill = "#0000FF")
    draw.line((17, 0, 17, amp[8]), fill = "#0000FF")
    
    draw.line((18, 0, 18, amp[9]), fill = "#7F00FF")
    draw.line((19, 0, 19, amp[9]), fill = "#7F00FF")

    draw.line((20, 0, 20, amp[10]), fill = "#FF00FF")
    draw.line((21, 0, 21, amp[10]), fill = "#FF00FF")
    
    draw.line((22, 0, 22, amp[11]), fill = "#FF007F")
    draw.line((23, 0, 23, amp[11]), fill = "#FF007F")

    draw.line((24, 0, 24, amp[12]), fill = "#FF0000")
    draw.line((25, 0, 25, amp[12]), fill = "#FF0000")
    
    draw.line((26, 0, 26, amp[13]), fill = "#FF8000")
    draw.line((27, 0, 27, amp[13]), fill = "#FF8000")

    draw.line((28, 0, 28, amp[14]), fill = "#FFFF00")
    draw.line((29, 0, 29, amp[14]), fill = "#FFFF00")
    
    draw.line((30, 0, 30, amp[15]), fill = "#80FF00")
    draw.line((31, 0, 31, amp[15]), fill = "#80FF00")
        
    matrix.SetImage(image.im.id, 0, 0)
    
#Start SPI communication
spi = spidev.SpiDev()
spi.open(0,1)
spi.bits_per_word = 8
spi.max_speed_hz = 100000
    
#Initialize GPIO pins & variables
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN)
GPIO.setup(25, GPIO.OUT, initial = GPIO.HIGH)
    
j = 0
maxAmp = 0
amp = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


#SPI communication & calling drawSpectrum to display values
while(1):
    for k in range(0,16):
        while(j < 2):
            piSpiEn = GPIO.input(24) 
            if(piSpiEn): #when the FPGA is done with FFT
                realData1 = spi.xfer([0x00])
                realData2 = spi.xfer([0x00])
                imagData1 = spi.xfer([0x00])
                imagData2 = spi.xfer([0x00])
                
                realDataNum1 = realData1[0]
                realDataNum2 = realData2[0]
                imagDataNum1 = imagData1[0]
                imagDataNum2 = imagData2[0]
                
            #Convert data from signed to unsigned values

                if(realDataNum2 > 127):
                    actualRealData2 = (realDataNum2 - 256) * 128
                else:
                    actualRealData2 = realDataNum2 * 128
                
                actualRealData = realDataNum1 + actualRealData2
                    
                if(imagDataNum2 > 127):
                    actualImagData2 = (imagDataNum2 - 256) * 128
                else:
                    actualImagData2 = imagDataNum2 * 128
                
                actualImagData = imagDataNum1 + actualImagData2
                
                #Tell FPGA the Pi is busy
                GPIO.output(25, GPIO.LOW)
                #Compute amplitudes
temp = math.sqrt(actualRealData**2 + 
actualImagData**2)
    temp = temp/1024
    if(maxAmp < temp):
        maxAmp = temp
                    
    #Tell FPGA the Pi can receive more data
GPIO.output(25, GPIO.HIGH)
    j += 1

j = 0
#Cast to an int before writing into array
    amp[k] = int(maxAmp)
    maxAmp = 0
    print amp[k]
    #Draw spectrum with the current int data in amp
drawSpectrum(amp)
spi.close()
