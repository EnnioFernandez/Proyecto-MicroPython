from machine import Pin, ADC, I2C
from time import sleep, time

# Configuración de pines
Pines= [0, 15, 2, 4, 16, 17, 5, 18, 19, 23, 13, 
        0, 12, 14, 27, 26, 25, 33, 32, 35]

DO = [Pin(pin, Pin.OUT) for pin in Pines[0:11]]  # Salidas digitales DO1 a DO10
Salidas= {
    "Husillo"    : DO[1], #Husillo
    "Ciclon"     : DO[2], #Ciclón
    "Carro"      : DO[3], #Carro
    "Inv Carro"  : DO[4], #Inversion de marcha del Carro
    "Vel rapida" : DO[5], #Velocidad ráída del Carro
    "Division"   : DO[6], #División
    "Bomba"      : DO[7], #Bomba hidráulica
    "EVB1 Up"    : DO[8], #Cilindro hacia arriba
    "EVB2 Down"  : DO[9], #Cilindro hacia abajo
    "Fin"        : DO[10] #Fin del ciclo
    }

DI = [Pin(pin, Pin.IN, Pin.PULL_DOWN) for pin in Pines[11:20]]  # Entradas digitales DI1 a DI8
Entradas = {
    "K1"    : DI[1],  #Fin de carrera +X
    "K2"    : DI[2], #Fin de carrera -X
    "K3"    : DI[3],  #Fin de carrera +Y
    "K4"    : DI[4],  #Fin de carrera -Y
    "PT"    : DI[5],  #Error Protección Térmica
    "PS"    : DI[6],  #Presostato
    "Start" : DI[7],  #Inicio de ciclo
    "MOdo"  : DI[8]  #Perilla modo automático/manual
    }

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
def mostrar(mensaje, linea=0):
    lcd.move_to(0, linea)
    lcd.write(mensaje)
    
# Función para activar una salida digital
def activar(salida):
    Salidas[salida].on()
    
# Función para desactivar una salida digital
def desactivar(salida):
    Salidas[salida].off()
    
# Función para leer entrada digital
def leer(entrada):
    return Entradas[entrada].value()
    
# Función para detener todas las salidas digitales
def detener_todo():
    for salida in DO:
        salida.off()

# Verificar posición inicial de K4 y K2
def verificar_posicion_inicial():
    if not leer("K4") or not leer("K2"):  # K4 y K2
        mostrar_mensaje("Error: Posición inicial")
        detener_todo()
        return False
    return True

# Leer los valores de los potenciómetros
def leer_potenciometro(ai):
    return (ai.read() / 4095) * 10  # Escala a 0-10 segundos

def main():
    while True:
        mostrar("funciona")
        lcd.write("hola")

        if leer("K1"):
            activar("Husillo")
        else:
            desactivar("Husillo")

main()