# Proyecto MicroPython
 
Informe automatización sensitiva
Para la automatización de la operación de corte de las rodajas de las camisas
de trapiche en lingotes, se utiliza como controlador principal un 
microcontrolador ESP 32, programado con micro Python, el cual secuencia mediante 
lógica programable y su reloj interno las fases del corte, las cuales, una vez colocada 
y centrada la rodaja sobre la mesa giratoria, serían las siguientes:

1.	Control de posicionamiento inicial de la herramienta, final de carrera 
superior del husillo activado (K4) y final de carrera del carro en -X activado (K2). 
De no cumplir con estas posiciones mostrará un error de posicionamiento inicial 
en pantalla y el operario deberá mover manualmente la herramienta a la posición original.
2.	Acercamiento del carro a plena velocidad (activando el relé R3 de 
velocidad rápida del VFD) hasta ubicar la herramienta de corte en el 
centro de la rodaja (motor M3), finalizado por un fin de carrera (K1), o 
lanzando un error si el tiempo de espera es superior a los 5 segundos y deteniendo el ciclo.
3.	Accionamiento del cilindro hidráulico para bajar la herramienta a posición 
de corte (electroválvula EVB1), hasta una posición determinada por temporizador 
regulable por un potenciómetro (P1) haciendo que la electroválvula quede en posición 
intermedia y bloqueando el cilindro. Máxima posición de bajada determinada por final 
de carrera (K3)
4.	Accionamiento del husillo (motor M1).
5.	Avance del carro (M3), con velocidad controlada por variador de 
frecuencia (VFD), ajustada a la máxima velocidad de corte permitida 
(por el potenciómetro P2, conectado directamente al variador), hasta topar 
con final de carrera (K2), o lanzando un error si el tiempo de espera es 
superior a los 25 segundos y deteniendo el ciclo.
6.	Accionamiento del cilindro hidráulico (EVB2), para subir la herramienta 
hasta posición de reposo, finalizado por final de carrera (K4).
7.	Apagado del husillo (M1).
8.	Inicio de la división accionado por motor con freno mecánico (M4), 
controlado por temporizador regulable (por el potenciómetro P2). 
9.	Se repite la operación desde el punto 1.
Para estos procesos además hacen falta que estén accionados los motores 
del ciclón (M2) y el de la bomba hidráulica (M5), ambos serán activados 
mediante perilla selectora en el tablero de control. A su vez el operario 
tambien tendrá la opción de controlar cada movimiento independiente en 
modo manual, mediante botonera en el tablero de control.  
El accionamiento de los contactores de trabajo se hace a través de relés 
de 12 VCA, que a su vez son accionados a través de optoacopladores por 
el microcontrolador ESP32. Las señales de los fines de carrera son 
alimentadas por 12 VCA, y estos accionan relés que tambien, a través 
de optoacopladores, entregan la señal al microcontrolador.

En total las salidas digitales (Digital Output, DO) del microcontrolador serán:

1-	DO1, para activar el contactor S1, que energiza el husillo, M1.
2-	DO2, para activar el relé R1, que activa el VFD, que energiza 
el carro, M3.
3-	DO3, para activar el relé R2, que activa la inversión de marcha 
del VFD, que energiza el carro, M3.
4-	DO4, para activar el relé R3, que activa la velocidad rápida 
del variador de frecuencia 
5-	DO5, para activar el contactor S5, que activa la división, M4.
6-	DO6, para activar el contactor S6, que activa la bomba hidráulica, M5.
7-	DO7, para activar el relé R4, que activa la bobina B1, 
para elevar el cilindro hidráulico.
8-	DO8, para activar el relé R5, que activa la bobina B2, 
para bajar el cilindro hidráulico.
9-	DO9, para desactivar el relé R12, marcando así el fin 
del ciclo de trabajo automático.


En total las entradas digitales (Digital Input, DI) del 
microcontrolador serán:

1-	DI1, detecta activación del relé R6, accionado por el 
fin de carrera +X, K1 del carro.
2-	DI2, detecta activación del relé R7, accionado por el 
fin de carrera -X, K2 del carro.
3-	DI3, detecta activación del relé R8, accionado por el 
fin de carrera inferior, K3 del cilindro.
4-	DI4, detecta activación del relé R9, accionado por el 
fin de carrera superior, K4 del carro.
5-	DI5, detecta la desactivación del relé R10, accionado 
por los contactos NC en serie de los térmicos, PT1, PT2, PT3, 
PT4, PT5 y el relé de error del VFD.
6-	DI6, detecta la activación del relé R11, accionado por el 
contacto NA del presostato de la bomba hidráulica, PS.
7-	DI7, detecta la activación del relé R12, accionado por un 
pulsador en el tablero de control, para activar el inicio del 
ciclo de trabajo automático.
8-	DI8, detecta la activación del relé R13, accionado por la 
perilla selectora de modo manual o automático.

En total las entradas analógicas (Analog Input, AI) del 
microcontrolador serán:

1-	AI1, detecta el potenciómetro P1, encargado de regular el 
tiempo de accionamiento de la bobina de la electroválvula, 
EVB1, en la bajada, entre 0 y 10 segundos.
2-	AI2, detecta el potenciómetro P3, encargado de regular el 
tiempo de la división, entre 0 y 10 segundos. 

Tambien tendrá un canal de comunicación con una pantalla LCD 14x2, 
con módulo I2C, el cual ocupará dos salidas digitales. El mismo 
servirá para visualizar los mensajes de error y sus tipos. 
1-	DO10, SCL.
2-	DO11, SDA.

En total 10 salidas digitales, 7 entradas digitales, 2 entradas 
analógicas y 2 pines para el canal de comunicación.
