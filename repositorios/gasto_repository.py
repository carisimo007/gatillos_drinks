from database.conexion import Conexion
from modelos.gasto import Gasto


class GastoRepository:

    def __init__(self):

        self.db = Conexion()

    def agregar(self, gasto):

        sql = """
        INSERT INTO gastos(

            fecha,
            descripcion,
            categoria_id,
            monto

        )

        VALUES(

            ?,?,?,?

        )
        """

        self.db.ejecutar(

            sql,

            (

                gasto.fecha,
                gasto.descripcion,
                gasto.categoria_id,
                gasto.monto

            )

        )

    def listar(self):

        sql = """
        SELECT

            gastos.id,
            gastos.fecha,
            categorias_gasto.nombre,
            gastos.descripcion,
            gastos.monto

        FROM gastos

        INNER JOIN categorias_gasto

            ON categorias_gasto.id = gastos.categoria_id

        ORDER BY gastos.fecha DESC,
                 gastos.id DESC
        """

        return self.db.consultar(sql)

    def buscar(self, texto):

        sql = """
        SELECT

            gastos.id,
            gastos.fecha,
            categorias_gasto.nombre,
            gastos.descripcion,
            gastos.monto

        FROM gastos

        INNER JOIN categorias_gasto

            ON categorias_gasto.id = gastos.categoria_id

        WHERE

            gastos.descripcion LIKE ?

            OR categorias_gasto.nombre LIKE ?

        ORDER BY gastos.fecha DESC,
                 gastos.id DESC
        """

        return self.db.consultar(

            sql,

            (

                f"%{texto}%",

                f"%{texto}%"

            )

        )

    def actualizar(self, gasto):

        sql = """
        UPDATE gastos

        SET

            fecha=?,
            descripcion=?,
            categoria_id=?,
            monto=?

        WHERE id=?
        """

        self.db.ejecutar(

            sql,

            (

                gasto.fecha,
                gasto.descripcion,
                gasto.categoria_id,
                gasto.monto,
                gasto.id

            )

        )

    def eliminar(self, id_gasto):

        sql = """
        DELETE FROM gastos

        WHERE id=?
        """

        self.db.ejecutar(

            sql,

            (

                id_gasto,

            )

        )

    def obtener_por_id(self, id_gasto):

        sql = """
        SELECT

            id,
            fecha,
            descripcion,
            categoria_id,
            monto

        FROM gastos

        WHERE id=?
        """

        registros = self.db.consultar(

            sql,

            (

                id_gasto,

            )

        )

        if not registros:

            return None

        fila = registros[0]

        return Gasto(

            id=fila[0],
            fecha=fila[1],
            descripcion=fila[2],
            categoria_id=fila[3],
            monto=fila[4]

        )