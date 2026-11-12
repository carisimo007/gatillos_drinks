class Producto:

    def __init__(
        self,
        id=None,
        nombre="",
        categoria="",
        precio_costo=0,
        precio_venta=0
    ):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.precio_costo = precio_costo
        self.precio_venta = precio_venta

    @property
    def precio_sugerido(self):
        return round(self.precio_costo * 1.30, 2)

    @property
    def ganancia(self):
        return round(self.precio_venta - self.precio_costo, 2)

    def __str__(self):
        return self.nombre