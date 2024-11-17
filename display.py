from machine import Pin, ADC, I2C
from time import sleep, time
from lcd1602 import LCD
import utime


# Configuración de I2C para la pantalla LCD
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
lcd = LCD(i2c, addr=0x27)