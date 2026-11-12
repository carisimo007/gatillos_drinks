from database.conexion import Conexion
from modelos.producto import Producto


class ProductoRepository:

    def __init__(self):
        self.db = Conexion()

    def agregar(self, producto):

        sql = """
        INSERT INTO productos
        (
            nombre,
            categoria,
            precio_costo,
            precio_venta
        )
        VALUES
        (
            ?, ?, ?, ?
        )
        """

        self.db.ejecutar(
            sql,
            (
                producto.nombre,
                producto.categoria,
                producto.precio_costo,
                producto.precio_venta
            )
        )

    def listar(self):

        sql = """
        SELECT
            id,
            nombre,
            categoria,
            precio_costo,
            precio_venta
        FROM productos
        ORDER BY nombre
        """

        registros = self.db.consultar(sql)

        productos = []

        for fila in registros:

            productos.append(

                Producto(

                    id=fila[0],
                    nombre=fila[1],
                    categoria=fila[2],
                    precio_costo=fila[3],
                    precio_venta=fila[4]

                )

            )

        return productos

    def buscar(self, texto):

        sql = """
        SELECT
            id,
            nombre,
            categoria,
            precio_costo,
            precio_venta
        FROM productos
        WHERE
            nombre LIKE ?
            OR categoria LIKE ?
        ORDER BY nombre
        """

        registros = self.db.consultar(
            sql,
            (
                f"%{texto}%",
                f"%{texto}%"
            )
        )

        productos = []

        for fila in registros:

            productos.append(

                Producto(

                    id=fila[0],
                    nombre=fila[1],
                    categoria=fila[2],
                    precio_costo=fila[3],
                    precio_venta=fila[4]

                )

            )

        return productos

    def actualizar(self, producto):

        sql = """
        UPDATE productos

        SET

            nombre=?,
            categoria=?,
            precio_costo=?,
            precio_venta=?

        WHERE id=?
        """

        self.db.ejecutar(

            sql,

            (

                producto.nombre,
                producto.categoria,
                producto.precio_costo,
                producto.precio_venta,
                producto.id

            )

        )

    def eliminar(self, id_producto):

        sql = """
        DELETE FROM productos
        WHERE id=?
        """

        self.db.ejecutar(
            sql,
            (id_producto,)
        )

    def obtener_por_id(self, id_producto):

        sql = """
        SELECT
            id,
            nombre,
            categoria,
            precio_costo,
            precio_venta
        FROM productos
        WHERE id=?
        """

        registro = self.db.consultar(sql, (id_producto,))

        if not registro:
            return None

        fila = registro[0]

        return Producto(

            id=fila[0],
            nombre=fila[1],
            categoria=fila[2],
            precio_costo=fila[3],
            precio_venta=fila[4]

        )