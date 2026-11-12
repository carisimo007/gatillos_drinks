class Venta:

    def __init__(

        self,

        id=None,
        fecha="",

        cliente="",

        producto_id=None,
        producto_nombre="",

        cantidad=1,

        costo_unitario=0,
        precio_unitario=0,

        subtotal=0,

        delivery=0,

        total=0

    ):

        self.id = id
        self.fecha = fecha

        self.cliente = cliente

        self.producto_id = producto_id
        self.producto_nombre = producto_nombre

        self.cantidad = cantidad

        self.costo_unitario = costo_unitario
        self.precio_unitario = precio_unitario

        self.subtotal = subtotal
        self.delivery = delivery
        self.total = total