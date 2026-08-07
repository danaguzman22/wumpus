class BaseConocimiento:
    
    def __init__(self):
        self.percepciones = {} # (x,y) -> {'breeze':.., 'stench':.., ...}
        self.seguras = {(1, 1)}
        self.peligrosas = set()
        self.posible_wumpus = set()
        self.visitadas = {(1, 1)}

    def registrar_percepcion(self, x, y, percepcion):
        self.percepciones[(x, y)] = percepcion
        self.visitadas.add((x, y))

    def marcar_segura(self, casilla):
        self.seguras.add(casilla)

    def marcar_peligrosa(self, casilla):
        self.peligrosas.add(casilla)

    def marcar_posible_wumpus(self, casilla):
        self.posible_wumpus.add(casilla)
        self.seguras.discard(casilla)

    def casillas_por_explorar(self):
        return self.seguras - self.visitadas - self.peligrosas - self.posible_wumpus