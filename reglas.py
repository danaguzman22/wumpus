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
    ENTONCES al menos una adyacente no confirmada-segura es sospechosa de pozo."""
    x, y = casilla
    percepcion = base.percepciones[casilla]
    conclusiones = []
    if percepcion['breeze']:
        vecinas = adyacentes(x, y)
        sospechosas = [v for v in vecinas if v not in base.seguras]
        if len(sospechosas) == 1:
            conclusiones.append(('peligrosa', sospechosas[0]))
    return conclusiones

# reglas activas del sistema, en el orden en que se evalúan
REGLAS = [regla_sin_breeze_ni_stench, regla_breeze]
