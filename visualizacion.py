import pygame
import sys
import os

TAMANIO_CASILLA = 150
ANCHO_VENTANA = TAMANIO_CASILLA * 4
ALTO_HUD = 80
ALTO_VENTANA = (TAMANIO_CASILLA * 4) + ALTO_HUD

COLOR_FONDO = (30, 30, 30)
COLOR_TEXTO = (255, 255, 255)
COLOR_VERDE_CLARO = (100, 255, 100)
COLOR_ROJO = (200, 60, 60)

imagenes = {}

def cargar_imagenes():
    archivos = {
        "piso_normal": "Piso.png",
        "piso_brillo": "piso oro.png",
        "pared": "pared.png",
        "agente": "agente.png",
        "agente_oro": "agente_oro.png",
        "agente_flecha": "agente_flecha.png",  # <-- Ya agregada acá
        "wumpus": "wumpus.png",
        "pozo": "hole.png",
        "oro": "oro.png",
        "brisa": "brisa.png",
        "hedor": "hedor.png"
    }
    
    # Cargar imágenes de las celdas
    for clave, nombre_archivo in archivos.items():
        ruta = os.path.join("images", nombre_archivo)
        try:
            img = pygame.image.load(ruta).convert_alpha()
            imagenes[clave] = pygame.transform.scale(img, (TAMANIO_CASILLA, TAMANIO_CASILLA))
        except FileNotFoundError:
            imagenes[clave] = pygame.Surface((TAMANIO_CASILLA, TAMANIO_CASILLA))
            imagenes[clave].fill((255, 0, 255)) 

    # Cargar pantallas especiales (Menú, Victoria y Derrota/Rendición)
    pantallas_especiales = {
        "menu_fondo": "menu_fondo.png",
        "fin_victoria": "fin_victoria.png",
        "fin_derrota": "fin_derrota.png"
    }
    
    for clave, nombre_archivo in pantallas_especiales.items():
        ruta = os.path.join("images", nombre_archivo)
        try:
            img = pygame.image.load(ruta).convert()
            imagenes[clave] = pygame.transform.scale(img, (ANCHO_VENTANA, ALTO_VENTANA))
        except FileNotFoundError:
            print(f"Aviso: No se encontró la imagen {ruta}. Se usará un fondo plano.")

def inicializar_pantalla():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Mundo del Wumpus - Motor de Inferencia")
    cargar_imagenes()
    return pantalla

def manejar_eventos():
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def dibujar_estado(pantalla, base, agente, tablero):
    pantalla.fill(COLOR_FONDO)
    
    oro_pos = tablero.get('oro') if isinstance(tablero, dict) else getattr(tablero, 'oro', None)
    wumpus_pos = tablero.get('wumpus') if isinstance(tablero, dict) else getattr(tablero, 'wumpus', None)
    pozos_pos = tablero.get('pozos', []) if isinstance(tablero, dict) else getattr(tablero, 'pozos', [])

    for x in range(1, 5):
        for y in range(1, 5):
            rect_x = (x - 1) * TAMANIO_CASILLA
            rect_y = (4 - y) * TAMANIO_CASILLA
            casilla = (x, y)
            
            # CAPA 0: Fondo
            if casilla == oro_pos:
                pantalla.blit(imagenes["piso_brillo"], (rect_x, rect_y))
            else:
                pantalla.blit(imagenes["piso_normal"], (rect_x, rect_y))
            
            # CAPA 1: Percepciones
            if hasattr(base, 'percepciones') and casilla in base.percepciones:
                if base.percepciones[casilla].get('breeze'):
                    pantalla.blit(imagenes["brisa"], (rect_x, rect_y))
                if base.percepciones[casilla].get('stench'):
                    pantalla.blit(imagenes["hedor"], (rect_x, rect_y))
                
            # CAPA 2: Objetos Reales
            if casilla == oro_pos and not getattr(agente, 'tiene_oro', False):
                pantalla.blit(imagenes["oro"], (rect_x, rect_y))
            if casilla in pozos_pos:
                pantalla.blit(imagenes["pozo"], (rect_x, rect_y))
            if casilla == wumpus_pos:
                pantalla.blit(imagenes["wumpus"], (rect_x, rect_y))
                
            # CAPA 3: Niebla de Guerra
            if casilla not in base.visitadas:
                pantalla.blit(imagenes["pared"], (rect_x, rect_y))
                
            # CAPA 4: Agente 
            if (agente.x, agente.y) == casilla:
                tiene_oro = getattr(agente, 'tiene_oro', False)
                tiene_flecha = getattr(agente, 'tiene_flecha', True)

                if tiene_oro:
                    pantalla.blit(imagenes["agente_oro"], (rect_x, rect_y))
                elif tiene_flecha and "agente_flecha" in imagenes:
                    pantalla.blit(imagenes["agente_flecha"], (rect_x, rect_y))
                else:
                    pantalla.blit(imagenes["agente"], (rect_x, rect_y))

    # DIBUJAR EL HUD
    fuente_hud = pygame.font.SysFont("arial", 24)
    tiene_oro = getattr(agente, 'tiene_oro', False)
    tiene_flecha = getattr(agente, 'tiene_flecha', True)
    texto_estado = f"Agente en: ({agente.x}, {agente.y}) | Oro: {'Sí' if tiene_oro else 'No'} | Flechas: {1 if tiene_flecha else 0}"
    superficie_texto = fuente_hud.render(texto_estado, True, COLOR_TEXTO)
    pantalla.blit(superficie_texto, (20, ALTO_VENTANA - ALTO_HUD + 25))

    pygame.display.flip()

def dibujar_menu(pantalla):
    if "menu_fondo" in imagenes:
        pantalla.blit(imagenes["menu_fondo"], (0, 0))
    else:
        pantalla.fill((30, 30, 30))
    pygame.display.flip()

def dibujar_fin(pantalla, mensaje_fin):
    if "VICTORIA" in mensaje_fin and "fin_victoria" in imagenes:
        pantalla.blit(imagenes["fin_victoria"], (0, 0))
    elif "fin_derrota" in imagenes:
        pantalla.blit(imagenes["fin_derrota"], (0, 0))
    else:
        pantalla.fill((30, 30, 30))
        
    pygame.display.flip()