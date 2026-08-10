class BaseConocimiento:

    def __init__(self):
        self.percepciones = {}              # (x,y) -> {'breeze':.., 'stench':.., ...}
        self.seguras_pozo = {(1, 1)}        # casillas sin pozo confirmado
        self.seguras_wumpus = {(1, 1)}      # casillas sin Wumpus confirmado
        self.seguras = {(1, 1)}             # casillas seguras para mover (interseccion)
        self.peligrosas = set()             # pozos confirmados
        self.posible_wumpus = set()         # Wumpus confirmado
        self.visitadas = {(1, 1)}
        self.sospecha_pozo = set()          # candidatas a pozo no confirmado
        self.sospecha_wumpus = set()        # candidatas a Wumpus no confirmado
        self.restricciones_pozo = {}        # (x,y) fuente -> set(candidatas a pozo)
        self.restricciones_wumpus = {}      # (x,y) fuente -> set(candidatas a Wumpus)
        self.wumpus_vivo = True             # si el Wumpus está muerto, el stench pierde valor
        self.casilla_oro_confirmada = None
        self.oro_recogido = False

    def registrar_percepcion(self, x, y, percepcion):
        self.percepciones[(x, y)] = percepcion
        self.visitadas.add((x, y))

    def _recalcular_seguras(self):
        self.seguras = self.seguras_pozo & self.seguras_wumpus

    def marcar_segura_pozo(self, casilla):
        self.seguras_pozo.add(casilla)
        self.sospecha_pozo.discard(casilla)
        self.peligrosas.discard(casilla)
        self._recalcular_seguras()

    def marcar_segura_wumpus(self, casilla):
        self.seguras_wumpus.add(casilla)
        self.sospecha_wumpus.discard(casilla)
        self.posible_wumpus.discard(casilla)
        self._recalcular_seguras()

    def marcar_segura(self, casilla):
        self.marcar_segura_pozo(casilla)
        self.marcar_segura_wumpus(casilla)

    def marcar_peligrosa(self, casilla):
        self.peligrosas.add(casilla)
        self.seguras_pozo.discard(casilla)
        self.seguras.discard(casilla)
        self.sospecha_pozo.discard(casilla)
        self._recalcular_seguras()

    def marcar_posible_wumpus(self, casilla):
        self.posible_wumpus.add(casilla)
        self.seguras_wumpus.discard(casilla)
        self.seguras.discard(casilla)
        self.sospecha_wumpus.discard(casilla)
        self._recalcular_seguras()

    def marcar_sospecha_pozo(self, casilla):
        if casilla not in self.seguras_pozo and casilla not in self.peligrosas:
            self.sospecha_pozo.add(casilla)

    def marcar_sospecha_wumpus(self, casilla):
        if casilla not in self.seguras_wumpus and casilla not in self.posible_wumpus:
            self.sospecha_wumpus.add(casilla)

    def limpiar_sospecha_pozo(self, casilla):
        self.sospecha_pozo.discard(casilla)

    def limpiar_sospecha_wumpus(self, casilla):
        self.sospecha_wumpus.discard(casilla)

    def registrar_restriccion_pozo(self, fuente, candidatas):
        self.restricciones_pozo[fuente] = set(candidatas)

    def registrar_restriccion_wumpus(self, fuente, candidatas):
        self.restricciones_wumpus[fuente] = set(candidatas)

    def limpiar_restriccion_pozo(self, fuente):
        self.restricciones_pozo.pop(fuente, None)

    def limpiar_restriccion_wumpus(self, fuente):
        self.restricciones_wumpus.pop(fuente, None)

    def interseccion_pozo(self):
        if not self.restricciones_pozo:
            return set()
        valores = [s for s in self.restricciones_pozo.values() if s]
        if not valores:
            return set()
        inter = set(valores[0])
        for candidatos in valores[1:]:
            inter &= candidatos
        return inter

    def interseccion_wumpus(self):
        if not self.restricciones_wumpus:
            return set()
        valores = [s for s in self.restricciones_wumpus.values() if s]
        if not valores:
            return set()
        inter = set(valores[0])
        for candidatos in valores[1:]:
            inter &= candidatos
        return inter

    def registrar_oro_recogido(self):
        self.oro_recogido = True

    def confirmar_oro(self, casilla):
        self.casilla_oro_confirmada = casilla

    def casillas_por_explorar(self):
        return (
            self.seguras
            - self.visitadas
            - self.peligrosas
            - self.posible_wumpus
            - self.sospecha_pozo
            - self.sospecha_wumpus
        )