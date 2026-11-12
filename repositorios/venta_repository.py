from database.conexion import Conexion
from modelos.venta import Venta


class VentaRepository:

    def __init__(self):

        self.db=Conexion()


    def agregar(self, venta):

        sql = """
        INSERT INTO ventas(

            fecha,
            cliente,

            producto_id,
            producto_nombre,

            cantidad,

            costo_unitario,
            precio_unitario,

            subtotal,
            delivery,
            total

        )

        VALUES(

            ?,?,?,?,?,?,?,?,?,?

        )
        """

        self.db.ejecutar(

            sql,

            (

                venta.fecha,

                venta.cliente,

                venta.producto_id,
                venta.producto_nombre,

                venta.cantidad,

                venta.costo_unitario,
                venta.precio_unitario,

                venta.subtotal,
                venta.delivery,
                venta.total

            )

        )


    def listar(self):

        sql = """
        SELECT

            id,
            fecha,
            cliente,
            producto_nombre,
            cantidad,
            costo_unitario,
            precio_unitario,
            subtotal,
            delivery,
            total

        FROM ventas

        ORDER BY id DESC
        """

        return self.db.consultar(sql)