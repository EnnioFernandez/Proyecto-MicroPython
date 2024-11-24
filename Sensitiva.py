from machine import Pin, ADC, I2C
from time import ticks_ms, sleep as delay

from i2c_lcd import I2cLcd


# Configuración de pines
Pines= [0, 2, 4, 15, 5, 17, 16, 18, 19, 
        0, 13, 12, 14, 27, 26, 25, 33, 23, 32]

# Pines de Salida digital DO
DO = [Pin(pin, Pin.OUT) for pin in Pines[0:9]]  # Salidas digitales DO1 a DO10
Salidas= {
    "Husillo"    : DO[1], #Husillo
    "Carro"      : DO[2], #Carro
    "Inv Carro"  : DO[3], #Inversion de marcha del Carro
    "Vel rapida" : DO[4], #Velocidad rápida del Carro
    "Division"   : DO[5], #División
    "EV Up"      : DO[6], #Cilindro hacia arriba
    "EV Down"    : DO[7], #Cilindro hacia abajo
    "Fin"        : DO[8]  #Fin del ciclo
    }

# Pines de entrada digital DI
DI = [Pin(pin, Pin.IN, Pin.PULL_DOWN) for pin in Pines[9:19]]  # Entradas digitales DI1 a DI8
Entradas = {
    "K1"    : DI[1],  #Fin de carrera +X
    "K2"    : DI[2],  #Fin de carrera -X
    "K3"    : DI[3],  #Fin de carrera +Y
    "K4"    : DI[4],  #Fin de carrera -Y
    "PT"    : DI[5],  #Error Protección Térmica
    "PS"    : DI[6],  #Presostato
    "Start" : DI[7],  #Inicio de ciclo
    "Modo"  : DI[8],  #Perilla modo automático/manual
    "Stop"  : DI[9]   #Parada de emergencia
    }

# Pines de entrada analógica AI   
AI1 = ADC(Pin(34))  # Potenciómetro P1 (regulación bajada EVB1)
AI2 = ADC(Pin(39))  # Potenciómetro P2 (regulación división)
AI3 = ADC(Pin(36))  # Potenciómetro P3 (regulación de la cantidad de cortes)

# Configuración de ADC para rango completo (0 a 3.3V)
AI1.atten(ADC.ATTN_11DB)
AI2.atten(ADC.ATTN_11DB)
AI3.atten(ADC.ATTN_11DB)

Potenciometro = {
    "P1"    :   AI1,    # Tiempo de bajada
    "P2"    :   AI2,    # Tiempo de división
    "P3"    :   AI3     # Número de cortes
}

# Configuración de I2C para la pantalla LCD
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=10000)     #initializing the I2C method for ESP32
lcd = I2cLcd(i2c, 0x27, 2, 16)

# Interrupción para cambio de numero de cortes
set_cortes= 0

def Cortes():
    global set_cortes
    if leer("P3", 11)+1 != set_cortes:
        print(int(leer("P3", 11)))
        mostrar_mensaje("Nro de cortes:")
        mostrar_mensaje("               ", 0, 1)
        mostrar_mensaje(str(int(leer("P3",11))+1), 10, 1)
        set_cortes = leer("P3", 11)+1

#Función para determinar el tiempo transcurrido en segundos
def time():
    return ticks_ms()/1000

# Función para mostrar mensajes en pantalla
def mostrar_mensaje(mensaje, fila=0, columna=0):
    lcd.move_to(fila, columna)
    lcd.putstr(mensaje)
    
# Función para activar una salida digital
def activar(salida1, salida2=None):
    Salidas[salida1].on()
    if salida2 is not None:
        Salidas[salida2].on()
    
# Función para desactivar una salida digital
def desactivar(salida1, salida2=None):
    Salidas[salida1].off()
    if salida2 is not None:
        Salidas[salida2].off()
    
# Función para leer entrada digital
def leer(entrada, escala=None):
    if entrada in ["P1", "P2", "P3"]:
        return (Potenciometro[entrada].read()/4095)*escala
    else:
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
def leer_potenciometro(ai, escala):
    return (potenciómetros[ai].read() / 4095) * escala  # Escala a 0-12 segundos

def Secuencia_automatica():
    #Paso 1: Verificación de posición inicial
    if not verificar_posicion_inicial():
        lcd.clear()
        mostrar_mensaje("Err1: falla posicion inicial")
        return

    # Paso 2: Acercamiento del carro rápidamente (R1, R3)
    lcd.clear()
    mostrar_mensaje("Moviendo a K1")
    activar("Carro", "Vel rapida")    # Activar carro a velocidad rápida(R1 y R3)
    inicio_tiempo = time()  # Inicia tiempo de espera
    while not leer("K1"):  # Espera por K1
        if time() - inicio_tiempo > 15:  # Timeout de 5 segundos
            lcd.clear()
            mostrar_mensaje("Err2: Timeout K1")
            detener_todo()
            return

    desactivar("Carro", "Vel rapida")  # Detener R1 y R3

    # Paso 3: Bajar herramienta (EVB2)
    lcd.clear()
    mostrar_mensaje("Bajando herramienta")
    inicio_tiempo= time()
    activar("EV Down")  # Activar B2
    while not leer("K3"):  #Espera por K3
        tiempo_bajada = leer("P1", 5)
        if time() - inicio_tiempo > tiempo_bajada:    
            break
    desactivar("EV Down")  # Detener B2

    # Paso 4: Encender husillo
    lcd.clear()
    mostrar_mensaje("Encendiendo husillo")
    activar("Husillo")  # Activar husillo M1

    # Paso 5: Avanzar carro a velocidad controlada
    lcd.clear()
    mostrar_mensaje("Avanzando a K2")
    activar("Carro")  # Activar avance (R1)
    inicio_tiempo = time()
    while not leer("K2"):  # Espera por K2
        if time() - inicio_tiempo > 25:  # Timeout de 25 segundos
            lcd.clear()
            mostrar_mensaje("Error: Timeout K2")
            detener_todo()
            return
    desactivar("Carro")  # Detener avance

    # Paso 6: Apagar husillo
    lcd.clear()
    mostrar_mensaje("Apagando husillo")
    desactivar("Husillo")

    # Paso 7: Subir herramienta (EVB2)
    lcd.clear()
    mostrar_mensaje("Subiendo herramienta")
    activar("EV Up")  # Activar bobina B1
    while not leer("K4"):  # Espera por K4
        delay(1)  # intervalo de espera
    desactivar("EV Up")  # Detener B1


    # Paso 8: Activar división
    lcd.clear()
    mostrar_mensaje("Inicio division")
    activar("Division")  # Activar división M4
    tiempo_division = leer("P2", 5)
    delay(tiempo_division)
    desactivar("Division")  # Detener M4

    # Repetir desde el paso 1
    mostrar_mensaje("Corte completado")
    delay(1)
 


def monitoreo(pin):
    detener_todo()
    while leer("PT") or leer("Stop") or leer("PS"):
        if leer("PT"):
            lcd.clear()
            mostrar_mensaje("Error 1:")
            mostrar_mensaje("Prot Termica", 0, 1)
            delay(2)
        
        if leer("PS"):
            lcd.clear()
            mostrar_mensaje("Error 2:")
            mostrar_mensaje("Presostato", 0, 1)
            delay(2)

        if leer("Stop"):
            lcd.clear()
            mostrar_mensaje("Error 3:")
            mostrar_mensaje("PARADA", 0, 1)
            delay(2)


        lcd.clear()

#   Interrupcion por PT:
DI[5].irq(trigger=Pin.IRQ_RISING, handler=monitoreo)    

#   Interrupción por PS:
DI[6].irq(trigger=Pin.IRQ_RISING, handler=monitoreo)

#   Interrupción por Stop:
DI[9].irq(trigger=Pin.IRQ_RISING, handler=monitoreo)    



def main():
    mostrar_mensaje("Sensitiva ON")
    while True:
        if leer("Modo"):
            print("Modo Automático OK")
            if leer("Start" ):
                print("Start OK")
                for i in range (leer("P1", 12)):
                    print("Secuencia OK. Corte: ", i+1)
                    Cortes()
                    Secuencia_automatica()
                mostrar_mensaje("Ciclo terminado")
                activar("Fin")
                delay(1)
                desactivar("Fin")
        
        else:
            print("Manual OK")
            Cortes()

main()