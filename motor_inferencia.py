from reglas import REGLAS

def _cambia_conocimiento(base, tipo, destino):
    """Determina si procesar la conclusión realmente agrega o
    modifica algún dato en la base de conocimiento."""
    chequeos = {
        'segura': destino not in base.seguras,
        'segura_pozo': destino not in base.seguras_pozo,
        'segura_wumpus': destino not in base.seguras_wumpus,
        'peligrosa_pozo': destino not in base.peligrosas,
        'peligrosa_wumpus': destino not in base.posible_wumpus,
        'sospecha_pozo': destino not in base.sospecha_pozo,
        'sospecha_wumpus': destino not in base.sospecha_wumpus,
        'limpiar_sospecha_pozo': destino in base.sospecha_pozo,
        'limpiar_sospecha_wumpus': destino in base.sospecha_wumpus,
        'oro_confirmado': base.casilla_oro_confirmada != destino,
    }
    return chequeos.get(tipo, False)

def aplicar_reglas(base):
    """Recorre las casillas visitadas, aplica reglas y devuelve
    una lista de trazas de las deducciones nuevas."""
    trazas = []
    mensajes = {
        "segura": "es segura",
        "segura_pozo": "es segura respecto a pozo",
        "segura_wumpus": "es segura respecto a Wumpus",
        "peligrosa_pozo": "es peligrosa por pozo",
        "peligrosa_wumpus": "es peligrosa por Wumpus",
        "sospecha_pozo": "es sospechosa de pozo",
        "sospecha_wumpus": "es sospechosa de Wumpus",
        "limpiar_sospecha_pozo": "deja de ser sospechosa de pozo",
        "limpiar_sospecha_wumpus": "deja de ser sospechosa de Wumpus",
        "oro_confirmado": "contiene el oro",
    }
    for casilla in base.visitadas:

        for regla in REGLAS:
            conclusiones = regla(casilla, base)

            for tipo, destino in conclusiones:
                if not _cambia_conocimiento(base, tipo, destino):
                    continue

                if tipo == 'segura':
                    base.marcar_segura(destino)
                elif tipo == 'segura_pozo':
                    base.marcar_segura_pozo(destino)
                elif tipo == 'segura_wumpus':
                    base.marcar_segura_wumpus(destino)
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
                elif tipo == 'oro_confirmado':
                    base.confirmar_oro(destino)

                destino_txt = f"({destino[0]},{destino[1]})"
                mensaje = mensajes.get(tipo, f"genera conclusion '{tipo}'")
                trazas.append(f"-> {regla.__name__} deduce: {destino_txt} {mensaje}")

    return trazas

def inferir(base):
    """Aplica las reglas repetidamente hasta que no surjan más
    conclusiones nuevas (punto fijo), igual que un motor
    de inferencia de un sistema experto.
    Devuelve una lista con todas las trazas deducidas."""
    trazas_totales = []
    while True:
        trazas_nuevas = aplicar_reglas(base)
        if not trazas_nuevas:
            break
        trazas_totales.extend(trazas_nuevas)
    return trazas_totales