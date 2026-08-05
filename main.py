from tablero import generar_tablero, percibir, adyacentes
from agente import Agente
from base_conocimiento import BaseConocimiento
from motor_inferencia import inferir

def elegir_accion(agente, base):
    candidatas = base.casillas_por_explorar()
    if candidatas:
        return ('mover', next(iter(candidatas)))
    return ('detener', None)


def simular():
    tablero = generar_tablero()
    agente = Agente()
    base = BaseConocimiento()
    paso = 1

    while agente.vivo and not agente.tiene_oro:
        percepcion = percibir(tablero, agente.x, agente.y)
        base.registrar_percepcion(agente.x, agente.y, percepcion)
        print(f"Paso {paso}: Agente en {(agente.x, agente.y)}. Percibe: {percepcion}")
        inferir(base)

        if percepcion['glitter']:
            agente.agarrar_oro()
            print(' -> Encontro el oro. Simulacion terminada con exito.')
            break

        accion, destino = elegir_accion(agente, base)
        if accion == 'mover':
            print(f' -> Accion elegida: mover a {destino} (casilla segura)')
            agente.mover_a(*destino)
        else:
            print(' -> No quedan casillas seguras por explorar. Fin de la simulacion.')
            break

        paso += 1

if __name__ == '__main__':
    simular()