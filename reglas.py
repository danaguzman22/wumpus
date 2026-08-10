from tablero import adyacentes

def regla_breeze(casilla, base):
    """Razonamiento para pozos:
    - SI no hay breeze, las adyacentes son seguras de pozo.
    - SI hay breeze, se generan candidatas y se triangula por interseccion."""
    percepcion = base.percepciones[casilla]
    conclusiones = []

    if not percepcion["breeze"]:
        base.limpiar_restriccion_pozo(casilla)
        for vecina in adyacentes(*casilla):
            conclusiones.append(("segura_pozo", vecina))
        return conclusiones

    sospechosas = [
        v for v in adyacentes(*casilla)
        if v not in base.seguras_pozo and v not in base.peligrosas
    ]
    base.registrar_restriccion_pozo(casilla, sospechosas)

    if len(sospechosas) == 1:
        conclusiones.append(("peligrosa_pozo", sospechosas[0]))
    else:
        for v in sospechosas:
            conclusiones.append(("sospecha_pozo", v))

    interseccion = base.interseccion_pozo()
    if len(interseccion) == 1:
        conclusiones.append(("peligrosa_pozo", next(iter(interseccion))))

    return conclusiones


def regla_stench(casilla, base):
    """Razonamiento para Wumpus con triangulación estricta por intersección de conjuntos."""
    percepcion = base.percepciones[casilla]
    conclusiones = []

    # SOLUCIÓN: Si el Wumpus está muerto, TODO alrededor es seguro respecto a él
    if not base.wumpus_vivo:
        base.limpiar_restriccion_wumpus(casilla)
        for vecina in adyacentes(*casilla):
            conclusiones.append(("segura_wumpus", vecina))
        return conclusiones

    if not percepcion["stench"]:
        base.limpiar_restriccion_wumpus(casilla)
        for vecina in adyacentes(*casilla):
            conclusiones.append(("segura_wumpus", vecina))
        return conclusiones

    sospechosas = [
        v for v in adyacentes(*casilla)
        if v not in base.seguras_wumpus
    ]
    base.registrar_restriccion_wumpus(casilla, sospechosas)

    interseccion = base.interseccion_wumpus()
    base.actualizar_candidatos_wumpus(interseccion)

    if len(interseccion) == 1:
        conclusiones.append(("peligrosa_wumpus", next(iter(interseccion))))

    return conclusiones


def regla_descartar_sospechas(casilla, base):
    """Descarta sospechas cuando ya hay seguridad parcial por tipo de peligro."""
    conclusiones = []

    if casilla in base.seguras_pozo and casilla in base.sospecha_pozo:
        conclusiones.append(("limpiar_sospecha_pozo", casilla))

    if casilla in base.seguras_wumpus and casilla in base.sospecha_wumpus:
        conclusiones.append(("limpiar_sospecha_wumpus", casilla))

    return conclusiones


def regla_glitter(casilla, base):
    """Si hay glitter, se confirma la localizacion del oro."""
    percepcion = base.percepciones[casilla]
    if percepcion.get("glitter"):
        return [("oro_confirmado", casilla)]
    return []


REGLAS = [regla_breeze, regla_stench, regla_descartar_sospechas, regla_glitter]
