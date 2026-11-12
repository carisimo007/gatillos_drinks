from database.conexion import Conexion


class InicializarBD:

    def __init__(self):

        self.db = Conexion()


    def crear_tablas(self):

        # ==========================
        # PRODUCTOS
        # ==========================

        self.db.ejecutar("""

        CREATE TABLE IF NOT EXISTS productos(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nombre TEXT NOT NULL,

            categoria TEXT NOT NULL,

            precio_costo REAL NOT NULL,

            precio_venta REAL NOT NULL

        )

        """)


        # ==========================
        # CLIENTES
        # ==========================

        self.db.ejecutar("""

        CREATE TABLE IF NOT EXISTS clientes(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nombre TEXT NOT NULL

        )

        """)


        # ==========================
        # VENTAS
        # ==========================

        self.db.ejecutar("""

        CREATE TABLE IF NOT EXISTS ventas(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            fecha TEXT NOT NULL,

            cliente TEXT NOT NULL,

            producto_id INTEGER NOT NULL,

            producto_nombre TEXT NOT NULL,

            cantidad INTEGER NOT NULL,

            costo_unitario REAL NOT NULL,

            precio_unitario REAL NOT NULL,

            subtotal REAL NOT NULL,

            delivery REAL NOT NULL,

            total REAL NOT NULL

        )

        """)


        # ==========================
        # CATEGORÍAS DE GASTOS
        # ==========================

        self.db.ejecutar("""

        CREATE TABLE IF NOT EXISTS categorias_gasto(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nombre TEXT NOT NULL UNIQUE,

            tipo TEXT NOT NULL,

            activo INTEGER NOT NULL DEFAULT 1

        )

        """)


        # ==========================
        # GASTOS
        # ==========================

        self.db.ejecutar("""

        CREATE TABLE IF NOT EXISTS gastos(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            fecha TEXT NOT NULL,

            descripcion TEXT NOT NULL,

            categoria_id INTEGER NOT NULL,

            monto REAL NOT NULL,

            FOREIGN KEY(categoria_id)
                REFERENCES categorias_gasto(id)

        )

        """)


        # ==========================
        # CARGAR CATEGORÍAS
        # ==========================

        self.cargar_categorias_por_defecto()


    def cargar_categorias_por_defecto(self):

        categorias = [

            ("Mercadería", "Compra"),

            ("Combustible", "Operativo"),

            ("Delivery", "Operativo"),

            ("Publicidad", "Operativo"),

            ("Insumos", "Operativo"),

            ("Mantenimiento", "Operativo"),

            ("Servicios", "Operativo"),

            ("Extras", "Operativo")

        ]

        for nombre, tipo in categorias:

            self.db.ejecutar(

                """
                INSERT OR IGNORE INTO categorias_gasto(
                    nombre,
                    tipo
                )
                VALUES(
                    ?,?
                )
                """,

                (
                    nombre,
                    tipo
                )

            )