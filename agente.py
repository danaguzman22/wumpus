class Agente:
    def __init__(self):
        self.x, self.y = 1, 1
        self.tiene_oro = False
        self.tiene_flecha = True
        self.vivo = True

    def mover_a(self, x, y):
        self.x, self.y = x, y

    def agarrar_oro(self):
        self.tiene_oro = True