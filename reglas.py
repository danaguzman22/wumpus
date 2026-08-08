from tablero import adyacentes

def regla_sin_breeze_ni_stench(casilla, base):
    """SI no hubo breeze ni stench en 'casilla'
    ENTONCES todas sus adyacentes son seguras."""
    x, y = casilla
    percepcion = base.percepciones[casilla]
    conclusiones = []
    if not percepcion['breeze'] and not percepcion['stench']:
        for vecina in adyacentes(x, y):
            conclusiones.append(('segura', vecina))
    return conclusiones

def regla_breeze(casilla, base):
    """SI hay breeze en 'casilla'
    ENTONCES al menos una adyacente no confirmada-segura es sospechosa de pozo.
    Si solo queda una sospechosa,
    entonces el pozo está confirmado.
    """
    x, y = casilla
    percepcion = base.percepciones[casilla]
    conclusiones = []
    if percepcion['breeze']:
        return conclusiones

    sospechosas = [
        v for v in adyacentes(*casilla)
        if v not in base.seguras]

    if len(sospechosas) == 1:

        conclusiones.append(
            ("peligrosa_pozo", sospechosas[0])
        )
    else:
        for v in sospechosas:
            conclusiones.append(
                ("sospecha_pozo", v)
            )
    return conclusiones


def regla_stench(casilla, base):
    """
    SI una casilla tiene Stench
    ENTONCES las casillas vecinas que aún no son seguras
    son sospechosas de contener el Wumpus.

    Si solo queda una sospechosa, entonces el Wumpus está confirmado.
    """

    percepcion = base.percepciones[casilla]
    conclusiones = []

    if not percepcion["stench"]:
        return conclusiones

    if not base.wumpus_vivo:
        return conclusiones

    sospechosas = [
        v for v in adyacentes(*casilla)
        if v not in base.seguras
    ]

    if len(sospechosas) == 1:
        conclusiones.append(
            ("peligrosa_wumpus", sospechosas[0])
        )

    else:
        for v in sospechosas:
            conclusiones.append(
                ("sospecha_wumpus", v)
            )

    return conclusiones

def regla_descartar_sospechas(casilla, base):
    """
    SI una casilla fue demostrada como segura
    ENTONCES deja de ser sospechosa
    tanto de pozo como de Wumpus.
    """

    conclusiones = []

    if casilla not in base.seguras:
        return conclusiones

    if casilla in base.sospecha_pozo:

        conclusiones.append(
            ("limpiar_sospecha_pozo", casilla)
        )

    if casilla in base.sospecha_wumpus:

        conclusiones.append(
            ("limpiar_sospecha_wumpus", casilla)
        )

    return conclusiones

REGLAS = [regla_sin_breeze_ni_stench, regla_breeze, regla_stench, regla_descartar_sospechas]
