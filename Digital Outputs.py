from machine import Pin, ADC, I2C
from time import sleep, time


# Configuración de pines
DO = [Pin(i, Pin.OUT) for i in range(10)]  # Salidas digitales DO1 a DO10
DI = [Pin(i + 12, Pin.IN, Pin.PULL_DOWN) for i in range(7)]  # Entradas digitales DI1 a DI7
AI1 = ADC(Pin(36))  # Potenciómetro P1 (regulación bajada EVB1)
AI2 = ADC(Pin(39))  # Potenciómetro P2 (regulación división)

# Configuración de ADC para rango completo (0 a 3.3V)
AI1.atten(ADC.ATTN_11DB)
AI2.atten(ADC.ATTN_11DB)

