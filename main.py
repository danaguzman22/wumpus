from tablero import generar_tablero, percibir, adyacentes
from agente import Agente
from base_conocimiento import BaseConocimiento
from motor_inferencia import inferir
import visualizacion
import pygame

def elegir_accion(agente, base):
    if agente.tiene_oro and (agente.x, agente.y) == (1, 1):
        return ('detener', None)
    
    candidatas = base.casillas_por_explorar()
    if candidatas:
        return ('mover', next(iter(candidatas)))
    return ('detener', None)


def simular():
    tablero = generar_tablero()
    agente = Agente()
    base = BaseConocimiento()
    paso = 1

    pantalla = visualizacion.inicializar_pantalla()
    simulacion_activa = True

    print("=== INICIO DE LA SIMULACIÓN MUNDO DEL WUMPUS ===\n")


    #while agente.vivo and not agente.tiene_oro:
    while simulacion_activa and agente.vivo:
        visualizacion.manejar_eventos()

        percepcion = percibir(tablero, agente.x, agente.y)
        base.registrar_percepcion(agente.x, agente.y, percepcion)

        # Etapa 1: Traza obligatoria en consola
        print(f"Paso {paso}: Agente en {(agente.x, agente.y)}. Percibe: {percepcion}")

        # Ejecución del Sistema Experto
        novedades_inferencia = inferir(base)

        # Etapa 2: Visualización
        visualizacion.dibujar_estado(pantalla, base, agente)
        pygame.time.delay(1500)  # Pausa de 1 segundo para ver la actualización

        # Acciones inmediatas
        if percepcion['glitter'] and not agente.tiene_oro:
            agente.agarrar_oro()
            print(' -> Encontro el oro. Simulacion terminada con exito.')
            paso += 1
            continue  # Salta a la siguiente iteración del bucle

        #Toma de desiciones 
        accion, destino = elegir_accion(agente, base)
        if accion == 'mover':
            print(f' -> Accion elegida: mover a {destino} (casilla segura)')
            agente.mover_a(*destino)

        elif accion == 'salir':
            print('-> Accion elegida: Salir de la cueva. Simulacion terminada con exito.')
            simulacion_activa = False
        else:
            print(' -> No quedan casillas seguras por explorar. Fin de la simulacion.')
            simulacion_activa = False

        paso += 1
        print("-"*50)

    print("Simulación finalizada.")

  # Bucle final infinito para que la ventana no se cierre sola al terminar
    while True:
        visualizacion.manejar_eventos()

if __name__ == '__main__':
    simular()