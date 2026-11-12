from database.inicializar import InicializarBD
from interfaz.principal import VentanaPrincipal


def main():

    # Crear base de datos y tablas si no existen
    bd = InicializarBD()
    bd.crear_tablas()

    # Iniciar aplicación gráfica
    app = VentanaPrincipal()
    app.iniciar()


if __name__ == "__main__":
    main()