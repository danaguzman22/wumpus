class Agente:
    def __init__(self):
        self.x, self.y = 1, 1
        self.tiene_oro = False
        self.tiene_flecha = True
        self.vivo = True
        self.direccion_grados = 90
        self.direccion = "este"

    def mover_a(self, x, y):
        self.x, self.y = x, y

    def agarrar_oro(self):
        self.tiene_oro = True

    def lanzar_flecha(self):
        self.tiene_flecha = False

    def girar_derecha(self):
        self.direccion_grados = (self.direccion_grados + 90) % 360
        direcciones = { 0: "norte", 90: "este", 180: "sur", 270: "oeste"}
        self.direccion = direcciones[self.direccion_grados]

    def girar_izquierda(self):
        self.direccion_grados = (self.direccion_grados - 90) % 360
        direcciones = { 0: "norte", 90: "este", 180: "sur", 270: "oeste"}
        self.direccion = direcciones[self.direccion_grados]

    def morir(self):
        self.vivo = False   

