

Pines = [0, 15, 2, 4, 16, 17, 5, 18, 19, 23, 13, 
         0, 12, 14, 27, 26, 25, 33, 32, 35]



DO= [pin for pin in Pines[0:11]]
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

DI= [pin for pin in Pines[11:20]]
print(Pines)
print("\n\n",DO, "\n")
print(DI, "\n")
print(DO[1], DO[10], "\n\n")
print(DI[1], DI[8], "\n\n")

def activar(Salida):
    print(Salidas[Salida])

def main():
    activar("Husillo")
    
main()