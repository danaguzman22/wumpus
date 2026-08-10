from tablero import generar_tablero, percibir, adyacentes, disparar, verificar_peligro
from agente import Agente
from base_conocimiento import BaseConocimiento
from motor_inferencia import inferir
from collections import deque
import visualizacion
import pygame
import os

def _direccion_hacia(origen, destino):
    x1, y1 = origen
    x2, y2 = destino
    if x2 > x1 and y1 == y2:
        return "este"
    if x2 < x1 and y1 == y2:
        return "oeste"
    if y2 > y1 and x1 == x2:
        return "norte"
    if y2 < y1 and x1 == x2:
        return "sur"
    return None


def _giro_necesario(direccion_actual, direccion_objetivo):
    grados = {"norte": 0, "este": 90, "sur": 180, "oeste": 270}
    delta = (grados[direccion_objetivo] - grados[direccion_actual]) % 360
    if delta == 0:
        return None
    if delta == 90:
        return "girar_derecha"
    if delta == 270:
        return "girar_izquierda"
    return "girar_derecha"


def _primer_paso_bfs(origen, destinos, transitables):
    """Devuelve el primer paso del camino mas corto desde origen
    hacia cualquier casilla en destinos usando solo transitables."""
    destinos = set(destinos)
    transitables = set(transitables)

    if not destinos:
        return None

    if origen in destinos:
        return origen

    transitables.add(origen)
    cola = deque([origen])
    padre = {origen: None}

    while cola:
        actual = cola.popleft()
        if actual in destinos:
            nodo = actual
            while padre[nodo] is not None and padre[nodo] != origen:
                nodo = padre[nodo]
            return nodo

        for vecina in adyacentes(*actual):
            if vecina not in transitables or vecina in padre:
                continue
            padre[vecina] = actual
            cola.append(vecina)

    return None


def elegir_accion(agente, base):
    # Si ya volvio al inicio con oro, debe salir.
    if agente.tiene_oro and (agente.x, agente.y) == (1, 1):
        return ("salir", None)

    # Si tiene oro, deja de explorar: solo intenta volver por seguras/visitadas.
    if agente.tiene_oro:
        transitables = (
            (base.visitadas | base.seguras)
            - base.peligrosas
            - base.posible_wumpus
        )
        destino = _primer_paso_bfs((agente.x, agente.y), {(1, 1)}, transitables)
        if destino is not None and destino != (agente.x, agente.y):
            direccion_objetivo = _direccion_hacia((agente.x, agente.y), destino)
            giro = _giro_necesario(agente.direccion, direccion_objetivo)
            if giro is not None:
                return (giro, None)
            return ("mover", destino)

        # Si no hay camino seguro conocido, no explora ni dispara.
        return ("detener", None)

    if agente.tiene_flecha and len(base.posible_wumpus) == 1:
        objetivo_wumpus = next(iter(base.posible_wumpus))
        direccion_objetivo = _direccion_hacia((agente.x, agente.y), objetivo_wumpus)
        if direccion_objetivo is not None:
            giro = _giro_necesario(agente.direccion, direccion_objetivo)
            if giro is not None:
                return (giro, None)
            return ("disparar", None)

    # 1. Obtener todas las casillas no visitadas
    candidatas_brutas = base.casillas_por_explorar()

    # 2. FILTRO DE SEGURIDAD ESTRICTO: 
    # Descartamos CUALQUIER casilla que tenga una sospecha o peligro de pozo/Wumpus.
    # El agente SOLO puede ir a casillas que sean 100% seguras o que no tengan ninguna alerta.
    candidatas_seguras_reales = [
        c for c in candidatas_brutas 
        if c not in base.sospecha_pozo 
        and c not in base.sospecha_wumpus 
        and c not in base.peligrosas
        and c not in base.posible_wumpus
    ]

    # Intentar ir primero a una adyacente que sea verdaderamente segura y libre de sospechas
    adyacentes_seguras = sorted(
        [casilla for casilla in adyacentes(agente.x, agente.y) if casilla in candidatas_seguras_reales]
    )
    if adyacentes_seguras:
        destino = adyacentes_seguras[0]
        direccion_objetivo = _direccion_hacia((agente.x, agente.y), destino)
        giro = _giro_necesario(agente.direccion, direccion_objetivo)
        if giro is not None:
            return (giro, None)
        return ("mover", destino)

    # Si no hay adyacentes seguras libres de sospecha, usar BFS pero SOLO usando transitables seguras
    transitables = (
        (base.visitadas | base.seguras)
        - base.peligrosas
        - base.posible_wumpus
        - base.sospecha_pozo
        - base.sospecha_wumpus
    )
    destino_bfs = _primer_paso_bfs((agente.x, agente.y), candidatas_seguras_reales, transitables)
    if destino_bfs is not None and destino_bfs != (agente.x, agente.y):
        direccion_objetivo = _direccion_hacia((agente.x, agente.y), destino_bfs)
        giro = _giro_necesario(agente.direccion, direccion_objetivo)
        if giro is not None:
            return (giro, None)
        return ("mover", destino_bfs)

    # Si no hay absolutamente ningúna opción limpia de sospechas, se detiene con elegancia
    return ("detener", None)

def simular():
    pygame.init() # Asegurate de tener esto para inicializar todos los módulos de pygame
    pygame.mixer.init() # Inicializa el mezclador de audio
    
    pantalla = visualizacion.inicializar_pantalla()
    reloj = pygame.time.Clock()
    
    # Cargar sonido del grito desde la carpeta sound
    try:
        sonido_grito = pygame.mixer.Sound(os.path.join("sound", "grito.mp3"))
    except Exception:
        sonido_grito = None
        print("Aviso: No se pudo cargar el archivo de audio del grito.")

    # Estados posibles: "MENU", "JUGANDO", "FIN"
    estado = "MENU"
    mensaje_fin = ""
    corriendo = True

    # Variables que se reinician en cada partida
    tablero = None
    agente = None
    base = None
    paso = 1

    while corriendo:
        if estado == "MENU":
            visualizacion.dibujar_menu(pantalla)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:  # Apretar ENTER
                        # Instanciamos todo de cero para una partida nueva
                        tablero = generar_tablero()
                        agente = Agente()
                        base = BaseConocimiento()
                        paso = 1
                        estado = "JUGANDO"
                        print("=== INICIO DE LA SIMULACIÓN MUNDO DEL WUMPUS ===\n")
                    elif evento.key == pygame.K_ESCAPE:
                        corriendo = False

        elif estado == "JUGANDO":
            # Procesar la "X" de la ventana para que no se cuelgue
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
            
            if not corriendo:
                break

            percepcion = percibir(tablero, agente.x, agente.y)
            base.registrar_percepcion(agente.x, agente.y, percepcion)

            # --- LIMPIEZA DE FANTASMAS ---
            # Si la celda es segura (no hay stench ni breeze), forzamos la limpieza de sospechas
            if not percepcion['stench'] and not percepcion['breeze']:
                base.limpiar_sospecha_pozo((agente.x, agente.y))
                base.limpiar_sospecha_wumpus((agente.x, agente.y))
                # También forzamos a marcarla como segura por si las dudas
                base.marcar_segura((agente.x, agente.y))
            # ------------------------------
            # Traza en consola
            print(f"Paso {paso}: Agente en {(agente.x, agente.y)}. Percibe: {percepcion}")
            if percepcion.get("scream"):
                print("  -> Se escucha un grito en la cueva (Scream).")

            # Ejecución del Sistema Experto
            trazas_inferencia = inferir(base)
            if trazas_inferencia:
                print("Inferencias del motor:")
                for traza in trazas_inferencia:
                    print(f"  {traza}")
            else:
                print("  -> Sin nuevas inferencias.")

            # Dibujamos y pasamos 'tablero'
            visualizacion.dibujar_estado(pantalla, base, agente, tablero)
            
            # AGREGAR ESTA LÍNEA PARA PAUSAR 1 SEGUNDO Y VER QUÉ HACE:
            pygame.time.delay(1000)

            # Acciones inmediatas
            if percepcion['glitter'] and not agente.tiene_oro:
                agente.agarrar_oro()
                base.registrar_oro_recogido()
                print(' -> Encontro el oro. Ahora debe regresar a (1, 1) y salir de la cueva.')
                paso += 1
                continue 

            # Toma de decisiones 
            accion, destino = elegir_accion(agente, base)
            
            if accion == 'mover':
                print(f' -> Accion elegida: mover a {destino} (casilla segura)')
                agente.mover_a(*destino)
                peligro = verificar_peligro(tablero, agente.x, agente.y)
                
                if peligro == "wumpus":
                    agente.morir()
                    visualizacion.dibujar_estado(pantalla, base, agente, tablero) # Dibujamos para que se vea dónde murió
                    print(" -> El agente entro en la casilla del Wumpus y murio. Derrota.")
                    mensaje_fin = "¡DERROTA! Te comió el Wumpus."
                    estado = "FIN"
                elif peligro == "pozo":
                    agente.morir()
                    visualizacion.dibujar_estado(pantalla, base, agente, tablero)
                    print(" -> El agente cayo en un pozo y murio. Derrota.")
                    mensaje_fin = "¡DERROTA! Caíste en un pozo."
                    estado = "FIN"
                    
            elif accion == 'girar_derecha':
                agente.girar_derecha()
                print(f' -> Accion elegida: girar a la derecha. Nueva direccion: {agente.direccion}')
            elif accion == 'girar_izquierda':
                agente.girar_izquierda()
                print(f' -> Accion elegida: girar a la izquierda. Nueva direccion: {agente.direccion}')

            elif accion == 'disparar':
                agente.lanzar_flecha()
                resultado_disparo = disparar(tablero, agente.x, agente.y, agente.direccion)
                
                if resultado_disparo == "Scream":
                    # Calculamos dónde estaba el Wumpus para limpiarlo de la base
                    wx, wy = agente.x, agente.y
                    if agente.direccion == "norte": wy += 1
                    elif agente.direccion == "sur": wy -= 1
                    elif agente.direccion == "este": wx += 1
                    elif agente.direccion == "oeste": wx -= 1
                    
                    # Llamamos al nuevo método limpio
                    base.notificar_wumpus_muerto((wx, wy))
                    
                    if sonido_grito:
                        sonido_grito.play()
                    
                    print(f' -> Accion elegida: disparar flecha. ¡Grito! El Wumpus en {(wx, wy)} murió.')
                else:
                    print(' -> Accion elegida: disparar flecha. Fallo el disparo.')  

            elif accion == 'salir':
                if agente.tiene_oro and (agente.x, agente.y) == (1, 1):
                    print('-> Accion elegida: Salir de la cueva con el oro. Victoria.')
                    mensaje_fin = "¡VICTORIA! Escapaste con el oro."
                else:
                    print('-> Accion elegida: Salir de la cueva sin oro.')
                    mensaje_fin = "RETIRADA. Saliste sin el oro."
                estado = "FIN"
                
            else: # Detener
                print(' -> No quedan casillas seguras por explorar. Fin de la simulacion.')
                mensaje_fin = "RENDICIÓN. Sin movimientos seguros."
                estado = "FIN"

            paso += 1
            if estado == "FIN":
                print("-" * 50)

        elif estado == "FIN":
            visualizacion.dibujar_fin(pantalla, mensaje_fin)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN: # Volver al menú
                        estado = "MENU"
                    elif evento.key == pygame.K_ESCAPE:
                        corriendo = False

    print("Simulación finalizada.")
    pygame.quit()

if __name__ == '__main__':
    simular()