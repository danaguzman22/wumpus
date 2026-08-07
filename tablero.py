import random

TAMANIO = 4


def generar_tablero(cant_pozos=2):
    if not 1 <= cant_pozos <= 3:
        raise ValueError("La cantidad de pozos debe estar entre 1 y 3.")

    casillas = [
        (x, y)
        for x in range(1, TAMANIO + 1)
        for y in range(1, TAMANIO + 1)
        if (x, y) != (1, 1)
    ]

    random.shuffle(casillas)

    wumpus = casillas.pop()
    pozos = [casillas.pop() for _ in range(cant_pozos)]
    oro = casillas.pop()

    return {
        "wumpus": wumpus,
        "pozos": pozos,
        "oro": oro,
    }


def adyacentes(x, y):
    candidatas = [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    ]

    return [
        (a, b)
        for a, b in candidatas
        if 1 <= a <= TAMANIO and 1 <= b <= TAMANIO
    ]


def percibir(tablero, x, y):
    if not (1 <= x <= TAMANIO and 1 <= y <= TAMANIO):
        raise ValueError("La posición está fuera del tablero.")

    vecinas = adyacentes(x, y)

    return {
    'breeze': any(v in tablero['pozos'] for v in vecinas),
    'stench': tablero['wumpus'] in vecinas,
    'glitter': (x, y) == tablero['oro'],
    }

def verificar_peligro(tablero, x, y):
    if (x, y) == tablero["wumpus"]:
        return "wumpus"
    if (x, y) in tablero["pozos"]:
        return "pozo"
    return None
