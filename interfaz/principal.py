import tkinter as tk
from tkinter import ttk

from interfaz.productos import VentanaProductos
from interfaz.ventas import VentanaVentas
from interfaz.gastos import VentanaGastos
from interfaz.caja import VentanaCaja


class VentanaPrincipal:

    def __init__(self):

        self.ventana = tk.Tk()

        self.ventana.title(
            "Gatillos Drinks"
        )

        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()

        ancho = int(ancho_pantalla * 0.90)
        alto = int(alto_pantalla * 0.90)

        x = (ancho_pantalla - ancho) // 2
        y = (alto_pantalla - alto) // 2

        self.ventana.geometry(
            f"{ancho}x{alto}+{x}+{y}"
        )

        self.ventana.minsize(
            1100,
            650
        )

        self.ventana.resizable(
            True,
            True
        )

        self.crear_interfaz()


    def crear_interfaz(self):

        # ==========================
        # CONTENEDOR PRINCIPAL
        # ==========================

        self.contenedor = tk.Frame(
            self.ventana
        )

        self.contenedor.pack(
            fill="both",
            expand=True
        )


        # ==========================
        # MENU LATERAL
        # ==========================

        self.menu = tk.Frame(
            self.contenedor,
            width=220
        )

        self.menu.pack(
            side="left",
            fill="y"
        )


        self.menu.pack_propagate(
            False
        )


        # ==========================
        # PANEL CENTRAL
        # ==========================

        self.panel = tk.Frame(
            self.contenedor
        )

        self.panel.pack(
            side="right",
            fill="both",
            expand=True
        )


        # ==========================
        # TITULO
        # ==========================

        titulo = tk.Label(
            self.menu,
            text="GATILLOS\nDRINKS",
            font=(
                "Arial",
                22,
                "bold"
            )
        )

        titulo.pack(
            pady=40
        )


        separador = ttk.Separator(
            self.menu,
            orient="horizontal"
        )

        separador.pack(
            fill="x",
            padx=20,
            pady=10
        )


        # ==========================
        # BOTONES MENU
        # ==========================


        boton_productos = ttk.Button(
            self.menu,
            text="📦  Productos",
            width=22,
            command=self.abrir_productos
        )

        boton_productos.pack(
            pady=8,
            padx=20
        )


        boton_clientes = ttk.Button(
            self.menu,
            text="👤  Clientes",
            width=22
        )

        boton_clientes.pack(
            pady=8,
            padx=20
        )


        boton_ventas = ttk.Button(
            self.menu,
            text="💰  Ventas",
            width=22,
            command=self.abrir_ventas
        )

        boton_ventas.pack(
            pady=8,
            padx=20
        )


        boton_gastos = ttk.Button(
            self.menu,
            text="💸  Gastos",
            width=22,
            command=self.abrir_gastos
        )

        boton_gastos.pack(
            pady=8,
            padx=20
        )

# ==========================
# BOTON CAJA
# ==========================

        boton_caja = ttk.Button(
            self.menu,
            text="📒 Caja",
            width=22,
            command=self.abrir_caja
        )

        boton_caja.pack(
            pady=8,
            padx=20
        )

        separador2 = ttk.Separator(
            self.menu,
            orient="horizontal"
        )

        separador2.pack(
            fill="x",
            padx=20,
            pady=20
        )


        boton_salir = ttk.Button(
            self.menu,
            text="🚪  Salir",
            width=22,
            command=self.ventana.destroy
        )

        boton_salir.pack(
            pady=10,
            padx=20
        )


        # ==========================
        # PANTALLA INICIAL
        # ==========================

        tarjeta = tk.Frame(
            self.panel
        )

        tarjeta.pack(
            pady=120
        )


        titulo_inicio = tk.Label(
            tarjeta,
            text="Bienvenido a",
            font=(
                "Arial",
                20
            )
        )

        titulo_inicio.pack()


        nombre = tk.Label(
            tarjeta,
            text="GATILLOS DRINKS",
            font=(
                "Arial",
                30,
                "bold"
            )
        )

        nombre.pack(
            pady=10
        )


        descripcion = tk.Label(
            tarjeta,
            text="Sistema de gestión de ventas y gastos",
            font=(
                "Arial",
                14
            )
        )

        descripcion.pack()



    # ==========================
    # PRODUCTOS
    # ==========================

    def abrir_productos(self):

        for widget in self.panel.winfo_children():

            widget.destroy()


        ventana_productos = VentanaProductos(
            self.panel
        )

        ventana_productos.mostrar()



    # ==========================
    # VENTAS
    # ==========================

    def abrir_ventas(self):

        for widget in self.panel.winfo_children():

            widget.destroy()


        ventana_ventas = VentanaVentas(
            self.panel
        )

        ventana_ventas.mostrar()



    # ==========================
    # GASTOS
    # ==========================

    def abrir_gastos(self):

        for widget in self.panel.winfo_children():

            widget.destroy()


        ventana_gastos = VentanaGastos(
            self.panel
        )

        ventana_gastos.mostrar()

# ==========================
# ABRIR CAJA
# ==========================

    def abrir_caja(self):

        for widget in self.panel.winfo_children():

            widget.destroy()


        ventana_caja = VentanaCaja(

            self.panel

        )

        ventana_caja.mostrar()

    # ==========================
    # INICIAR
    # ==========================

    def iniciar(self):

        self.ventana.mainloop()