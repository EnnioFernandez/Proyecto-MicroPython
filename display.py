from machine import Pin, I2C, ADC
from time import sleep_ms as delay
from lcd1602 import LCD

# Inicializa el bus I2C
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

# Dirección del módulo LCD (cambiar si es distinta)
lcd = LCD(i2c, addr=0x27)
