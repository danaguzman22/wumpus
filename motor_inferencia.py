from reglas import REGLAS

def _cambia_conocimiento(base, tipo, destino):
    """Determina si procesar la conclusión realmente agrega o
    modifica algún dato en la base de conocimiento."""
    chequeos = {
        'segura': destino not in base.seguras,
        'peligrosa_pozo': destino not in base.peligrosas,
        'peligrosa_wumpus': destino not in base.posible_wumpus,
        'sospecha_pozo': destino not in base.sospecha_pozo,
        'sospecha_wumpus': destino not in base.sospecha_wumpus,
        'limpiar_sospecha_pozo': destino in base.sospecha_pozo,
        'limpiar_sospecha_wumpus': destino in base.sospecha_wumpus,
    }
    return chequeos.get(tipo, False)

def aplicar_reglas(base):
    """Recorre todas las casillas visitadas y dispara cada regla.
    Devuelve True si se agregó conocimiento nuevo (para repetir
    el ciclo, tal como hace un motor de encadenamiento hacia adelante)."""
    hubo_novedades = False
    for casilla in base.visitadas:

        for regla in REGLAS:
            conclusiones = regla(casilla, base)

            for tipo, destino in conclusiones:
                if not _cambia_conocimiento(base, tipo, destino):
                    continue

                if tipo == 'segura':
                    base.marcar_segura(destino)
                elif tipo == 'peligrosa_pozo':
                    base.marcar_peligrosa(destino)
                elif tipo == 'peligrosa_wumpus':
                    base.marcar_posible_wumpus(destino)
                elif tipo == 'sospecha_pozo':
                    base.marcar_sospecha_pozo(destino)
                elif tipo == 'sospecha_wumpus':
                    base.marcar_sospecha_wumpus(destino)
                elif tipo == 'limpiar_sospecha_pozo':
                    base.limpiar_sospecha_pozo(destino)
                elif tipo == 'limpiar_sospecha_wumpus':
                    base.limpiar_sospecha_wumpus(destino)

                hubo_novedades = True

    return hubo_novedades

def inferir(base):
    """Aplica las reglas repetidamente hasta que no surjan más
    conclusiones nuevas (punto fijo), igual que un motor
    de inferencia de un sistema experto.
    Devuelve la cantidad total de novedades deducidas."""
    total_novedades = 0
    while True:
        novedades = aplicar_reglas(base)
        total_novedades += novedades
        if not novedades:
            break
    return total_novedades