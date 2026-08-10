class BaseConocimiento:

    def __init__(self):
        self.percepciones = {}              # (x,y) -> {'breeze':.., 'stench':.., ...}
        self.seguras = {(1, 1)}             # casillas confirmadas libres de peligro
        self.peligrosas = set()             # pozos confirmados
        self.posible_wumpus = set()         # Wumpus confirmado
        self.visitadas = {(1, 1)}
        self.sospecha_pozo = set()          # candidatas a pozo no confirmado
        self.sospecha_wumpus = set()        # candidatas a Wumpus no confirmado
        self.wumpus_vivo = True             # si el Wumpus está muerto, el stench pierde valor

    def registrar_percepcion(self, x, y, percepcion):
        self.percepciones[(x, y)] = percepcion
        self.visitadas.add((x, y))

    def marcar_segura(self, casilla):
        self.seguras.add(casilla)
        self.sospecha_pozo.discard(casilla)
        self.sospecha_wumpus.discard(casilla)

    def marcar_peligrosa(self, casilla):
        self.peligrosas.add(casilla)
        self.seguras.discard(casilla)
        self.sospecha_pozo.discard(casilla)
        self.sospecha_wumpus.discard(casilla)

    def marcar_posible_wumpus(self, casilla):
        self.posible_wumpus.add(casilla)
        self.seguras.discard(casilla)
        self.sospecha_pozo.discard(casilla)
        self.sospecha_wumpus.discard(casilla)

    def marcar_sospecha_pozo(self, casilla):
        if casilla not in self.seguras and casilla not in self.peligrosas:
            self.sospecha_pozo.add(casilla)

    def marcar_sospecha_wumpus(self, casilla):
        if casilla not in self.seguras and casilla not in self.posible_wumpus:
            self.sospecha_wumpus.add(casilla)

    def limpiar_sospecha_pozo(self, casilla):
        self.sospecha_pozo.discard(casilla)

    def limpiar_sospecha_wumpus(self, casilla):
        self.sospecha_wumpus.discard(casilla)

    def casillas_por_explorar(self):
        return (self.seguras - self.visitadas - self.peligrosas
                - self.posible_wumpus - self.sospecha_pozo - self.sospecha_wumpus)