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
def activar_salida(index, tiempo=None):
    DO[index].on()
    if tiempo:
        sleep(tiempo)
        DO[index].off()

# Función para detener todas las salidas digitales
def detener_todo():
    for salida in DO:
        salida.off()

# Verificar posición inicial de K4 y K2
def verificar_posicion_inicial():
    if not DI[4].value() or not DI[2].value():  # K4 y K2
        mostrar_mensaje("Error: Posición inicial")
        detener_todo()
        return False
    return True

# Leer los valores de los potenciómetros
def leer_potenciometro(ai):
    return (ai.read() / 4095) * 10  # Escala a 0-10 segundos

# Secuencia de automatización
def secuencia_automatica():
    # Paso 1: Verificar posición inicial
    if not verificar_posicion_inicial():
        return

    # Paso 2: Acercamiento del carro rápidamente (R3)
    mostrar_mensaje("Moviendo a K1")
    activar_salida(5)  # Activar velocidad rápida (R3)
    inicio_tiempo = time()
    while not DI[1].value():  # Espera por K1
        if time() - inicio_tiempo > 5:  # Timeout de 5 segundos
            mostrar_mensaje("Error: Timeout K1")
            detener_todo()
            return
    DO[5].off()  # Detener R3

    # Paso 3: Bajar herramienta (EVB2)
    mostrar_mensaje("Bajando herramienta")
    inicio_tiempo= time()
    while not DI[3].value():  #Espera por K3
        tiempo_bajada = leer_potenciometro(AI1)
        if time() - inicio_tiempo > tiempo_bajada:
            
        
    activar_salida(9)  # Activar bobina B2
    tiempo_bajada = leer_potenciometro(AI1)
    sleep(tiempo_bajada)
    if not DI[2].value():  # Verificar K3
        mostrar_mensaje("Error: K3 no activado")
        detener_todo()
        return
    DO[8].off()  # Detener B2

    # Paso 4: Encender husillo
    mostrar_mensaje("Encendiendo husillo")
    activar_salida(0)  # Activar husillo M1

    # Paso 5: Avanzar carro a velocidad controlada
    mostrar_mensaje("Avanzando a K2")
    activar_salida(3)  # Activar avance (R1)
    inicio_tiempo = time()
    while not DI[1].value():  # Espera por K2
        if time() - inicio_tiempo > 25:  # Timeout de 25 segundos
            mostrar_mensaje("Error: Timeout K2")
            detener_todo()
            return
    DO[3].off()  # Detener avance

    # Paso 6: Subir herramienta (EVB2)
    mostrar_mensaje("Subiendo herramienta")
    activar_salida(9)  # Activar bobina B1
    while not DI[3].value():  # Espera por K4
        sleep(0.1)  # Polling interval
    DO[9].off()  # Detener B1

    # Paso 7: Apagar husillo
    mostrar_mensaje("Apagando husillo")
    DO[0].off()

    # Paso 8: Activar división
    mostrar_mensaje("Inicio división")
    activar_salida(5)  # Activar división M4
    tiempo_division = leer_potenciometro(AI2)
    sleep(tiempo_division)
    DO[5].off()  # Detener M4

    # Repetir desde el paso 1
    mostrar_mensaje("Ciclo completado")
    sleep(2)

# Modo manual
def modo_manual():
    mostrar_mensaje("Modo Manual")
    while True:
        # Implementar control manual desde botones
        if DI[6].value():  # Botón de inicio manual
            mostrar_mensaje("Operación manual")
            sleep(1)
            break

# Programa principal
while True:
    if DI[6].value():  # Botón de inicio automático
        secuencia_automatica()
    else:
        modo_manual()
