from machine import Pin, ADC, I2C
from time import sleep, time
import utime

# Configuración de pines
Pines= [0, 15, 2, 4, 16, 17, 5, 18, 19, 23, 13
        0, 12, 14, 27, 26, 25, 33, 32, 35]

DO = [Pin(pin, Pin.OUT) for pin in Pines[0:10]]  # Salidas digitales DO1 a DO10
#D0[1]: Husillo
#D0[2]: Ciclón
#D0[3]: VFD-Carro
#D0[4]: Inversión-VFD
#D0[5]: Velocidad Rápida VFD
#D0[6]: División
#D0[7]: Bomba hidráulica
#D0[8]: Bobina EVB1
#D0[9]: Bobina EVB2
#D0[10]: Fin de ciclo

DI = [Pin(pin, Pin.IN, Pin.PULL_DOWN) for pin in Pines[11:20]]  # Entradas digitales DI1 a DI8
#DI[1]: K1-Fin de carrera +X
#DI[2]: K2-Fin de carrera -X
#DI[3]: K3-Fin de carrera +Y
#DI[4]: K4-Fin de carrera -Y
#DI[5]: Error Protección Térmica
#DI[6]: Presostato
#DI[7]: Inicio de ciclo
#DI[8]: Perilla modo automático/manual

AI1 = ADC(Pin(36))  # Potenciómetro P1 (regulación bajada EVB1)
AI2 = ADC(Pin(39))  # Potenciómetro P2 (regulación división)

# Configuración de ADC para rango completo (0 a 3.3V)
AI1.atten(ADC.ATTN_11DB)
AI2.atten(ADC.ATTN_11DB)

# Configuración de I2C para la pantalla LCD
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
from lcd1602 import LCD  # Asegúrate de incluir la librería para LCD
lcd = LCD(i2c, addr=0x27)

# Función para mostrar mensajes en pantalla
def mostrar_mensaje(mensaje, linea=0):
    lcd.move_to(0, linea)
    lcd.clear_line(linea)
    lcd.write(mensaje[:16])
    
# Función para activar una salida digital
def activar(salida, tiempo=None):
    DO[index].on()
    if tiempo:
        sleep(tiempo)
        DO[index].off()
