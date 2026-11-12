from database.conexion import Conexion


class CajaRepository:

    def __init__(self):

        self.db = Conexion()


    def listar(self, fecha_desde, fecha_hasta):

        sql = """

        SELECT

            fecha,

            'INGRESO',

            cliente,

            producto_nombre,

            subtotal

        FROM ventas


        UNION ALL


        SELECT

            fecha,

            'GASTO',

            '',

            descripcion,

            monto

        FROM gastos

        """

        registros = self.db.consultar(sql)

        movimientos = []

        desde = self.convertir_fecha(fecha_desde)

        hasta = self.convertir_fecha(fecha_hasta)

        for registro in registros:

            fecha = registro[0]

            fecha_convertida = self.convertir_fecha(fecha)

            if desde <= fecha_convertida <= hasta:

                movimientos.append(registro)

        movimientos.sort(
            key=lambda x: self.convertir_fecha(x[0])
        )

        return movimientos



    def convertir_fecha(self, fecha):

        fecha = fecha.split(" ")[0]

        if "/" in fecha:

            dia, mes, año = fecha.split("/")

        else:

            dia, mes, año = fecha.split("-")

        return año + mes + dia