from database.conexion import Conexion
from modelos.categoria_gasto import CategoriaGasto


class CategoriaGastoRepository:

    def __init__(self):

        self.db = Conexion()


    def listar(self):

        sql = """
        SELECT

            id,
            nombre,
            tipo,
            activo

        FROM categorias_gasto

        WHERE activo=1

        ORDER BY nombre
        """

        registros = self.db.consultar(sql)

        categorias = []

        for fila in registros:

            categorias.append(

                CategoriaGasto(

                    id=fila[0],

                    nombre=fila[1],

                    tipo=fila[2],

                    activo=fila[3]

                )

            )

        return categorias


    def agregar(self, categoria):

        sql = """
        INSERT INTO categorias_gasto(

            nombre,

            tipo

        )

        VALUES(

            ?,?

        )
        """

        self.db.ejecutar(

            sql,

            (

                categoria.nombre,

                categoria.tipo

            )

        )


    def actualizar(self, categoria):

        sql = """
        UPDATE categorias_gasto

        SET

            nombre=?,

            tipo=?,

            activo=?

        WHERE id=?
        """

        self.db.ejecutar(

            sql,

            (

                categoria.nombre,

                categoria.tipo,

                categoria.activo,

                categoria.id

            )

        )


    def desactivar(self, id_categoria):

        sql = """
        UPDATE categorias_gasto

        SET activo=0

        WHERE id=?
        """

        self.db.ejecutar(

            sql,

            (

                id_categoria,

            )

        )


    def obtener_por_id(self, id_categoria):

        sql = """
        SELECT

            id,

            nombre,

            tipo,

            activo

        FROM categorias_gasto

        WHERE id=?
        """

        registros = self.db.consultar(

            sql,

            (

                id_categoria,

            )

        )

        if not registros:

            return None

        fila = registros[0]

        return CategoriaGasto(

            id=fila[0],

            nombre=fila[1],

            tipo=fila[2],

            activo=fila[3]

        )