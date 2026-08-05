import pygame
import sys

TAMANIO_CASILLA = 150
MARGEN = 5
ANCHO_VENTANA = TAMANIO_CASILLA * 4
ALTO_VENTANA = TAMANIO_CASILLA * 4

# Paleta de colores
COLOR_FONDO = (30, 30, 30)
COLOR_DESCONOCIDO = (70, 70, 70)
COLOR_SEGURA = (80, 180, 80)
COLOR_PELIGROSA = (200, 60, 60)
COLOR_VISITADA = (50, 120, 50)
COLOR_AGENTE = (50, 150, 255)
COLOR_TEXTO = (255, 255, 255)

def inicializar_pantalla():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Mundo del Wumpus - Motor de Inferencia")
    return pantalla

def manejar_eventos():
    """Mantiene la ventana responsiva y permite cerrarla con la 'X'."""
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def dibujar_estado(pantalla, base, agente):
    pantalla.fill(COLOR_FONDO)
    fuente = pygame.font.SysFont(None, 48)

    for x in range(1, 5):
        for y in range(1, 5):
            # Inversión del eje Y: (1,1) va abajo a la izquierda
            rect_x = (x - 1) * TAMANIO_CASILLA + MARGEN
            rect_y = (4 - y) * TAMANIO_CASILLA + MARGEN
            ancho_rect = TAMANIO_CASILLA - (MARGEN * 2)

            casilla = (x, y)
            color = COLOR_DESCONOCIDO
            texto = "?"

            # Determinar color según la Base de Conocimiento
            if casilla in base.visitadas:
                color = COLOR_VISITADA
                texto = "V"
            elif casilla in base.peligrosas:
                color = COLOR_PELIGROSA
                texto = "P"
            elif casilla in base.seguras:
                color = COLOR_SEGURA
                texto = "S"

            # Dibujar fondo de la casilla
            pygame.draw.rect(pantalla, color, (rect_x, rect_y, ancho_rect, ancho_rect), border_radius=10)
            
            # Dibujar al agente como un círculo azul si está en esta casilla
            if (agente.x, agente.y) == casilla:
                pygame.draw.circle(pantalla, COLOR_AGENTE, (rect_x + ancho_rect//2, rect_y + ancho_rect//2), ancho_rect//3)
                texto = "A"

            # Renderizar el texto centrado
            superficie_texto = fuente.render(texto, True, COLOR_TEXTO)
            rect_texto = superficie_texto.get_rect(center=(rect_x + ancho_rect//2, rect_y + ancho_rect//2))
            pantalla.blit(superficie_texto, rect_texto)

    pygame.display.flip()