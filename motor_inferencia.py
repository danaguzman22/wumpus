from reglas import REGLAS

def aplicar_reglas(base):
    """Recorre todas las casillas visitadas y dispara cada regla.
    Devuelve True si se agregó conocimiento nuevo (para repetir
    el ciclo, tal como hace un motor de encadenamiento hacia adelante)."""
    hubo_novedades = False
    for casilla in base.visitadas:

        for regla in REGLAS:
            conclusiones = regla(casilla, base)

            for tipo, destino in conclusiones:
                if tipo == 'segura' and destino not in base.seguras:
                    base.marcar_segura(destino)
                    hubo_novedades = True
                elif tipo == 'peligrosa' and destino not in base.peligrosas:
                    base.marcar_peligrosa(destino)
                    hubo_novedades = True
                elif tipo == 'wumpus' and destino not in base.posible_wumpus:
                    base.marcar_posible_wumpus(destino)
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
