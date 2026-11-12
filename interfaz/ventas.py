import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from modelos.venta import Venta
from repositorios.venta_repository import VentaRepository
from repositorios.producto_repository import ProductoRepository


class VentanaVentas:

    def __init__(self, contenedor):

        self.contenedor = contenedor

        self.venta_repository = VentaRepository()
        self.producto_repository = ProductoRepository()

        self.productos = []

    def mostrar(self):

        for widget in self.contenedor.winfo_children():
            widget.destroy()

        titulo = tk.Label(
            self.contenedor,
            text="Gestión de Ventas",
            font=("Arial",18,"bold")
        )

        titulo.pack(pady=10)

        formulario = tk.LabelFrame(
            self.contenedor,
            text="Nueva Venta",
            padx=10,
            pady=10
        )

        formulario.pack(
            fill="x",
            padx=15,
            pady=10
        )

        tk.Label(
            formulario,
            text="Cliente"
        ).grid(row=0,column=0,padx=5,pady=5,sticky="w")

        self.txt_cliente = tk.Entry(
            formulario,
            width=35
        )

        self.txt_cliente.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        tk.Label(
            formulario,
            text="Producto"
        ).grid(row=1,column=0,padx=5,pady=5,sticky="w")

        self.cmb_producto = ttk.Combobox(
            formulario,
            width=32,
            state="readonly"
        )

        self.cmb_producto.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        self.productos = self.producto_repository.listar()

        self.cmb_producto["values"] = [

            p.nombre

            for p in self.productos

        ]

        self.cmb_producto.bind(
            "<<ComboboxSelected>>",
            self.cambiar_producto
        )

        tk.Label(
            formulario,
            text="Cantidad"
        ).grid(row=2,column=0,padx=5,pady=5,sticky="w")

        self.sp_cantidad = tk.Spinbox(
            formulario,
            from_=1,
            to=999,
            width=8,
            command=self.calcular_total
        )

        self.sp_cantidad.grid(
            row=2,
            column=1,
            sticky="w",
            padx=5,
            pady=5
        )

        self.sp_cantidad.bind(
            "<KeyRelease>",
            self.calcular_total
        )

        tk.Label(
            formulario,
            text="Precio Unitario"
        ).grid(row=3,column=0,padx=5,pady=5,sticky="w")

        self.txt_precio = tk.Entry(
            formulario,
            state="readonly",
            width=15
        )

        self.txt_precio.grid(
            row=3,
            column=1,
            sticky="w",
            padx=5,
            pady=5
        )

        tk.Label(
            formulario,
            text="Subtotal"
        ).grid(row=4,column=0,padx=5,pady=5,sticky="w")

        self.txt_subtotal = tk.Entry(
            formulario,
            state="readonly",
            width=15
        )

        self.txt_subtotal.grid(
            row=4,
            column=1,
            sticky="w",
            padx=5,
            pady=5
        )

        self.delivery = tk.BooleanVar()

        self.chk_delivery = tk.Checkbutton(

            formulario,

            text="Delivery",

            variable=self.delivery,

            command=self.calcular_total

        )

        self.chk_delivery.grid(
            row=5,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        tk.Label(
            formulario,
            text="Costo Delivery"
        ).grid(row=6,column=0,padx=5,pady=5,sticky="w")

        self.txt_delivery = tk.Entry(
            formulario,
            width=15
        )

        self.txt_delivery.insert(
            0,
            "0"
        )

        self.txt_delivery.grid(
            row=6,
            column=1,
            sticky="w",
            padx=5,
            pady=5
        )

        self.txt_delivery.bind(
            "<KeyRelease>",
            self.calcular_total
        )

        tk.Label(
            formulario,
            text="TOTAL",
            font=("Arial",12,"bold")
        ).grid(row=7,column=0,padx=5,pady=10,sticky="w")

        self.txt_total = tk.Entry(
            formulario,
            state="readonly",
            width=15
        )

        self.txt_total.grid(
            row=7,
            column=1,
            sticky="w",
            padx=5,
            pady=10
        )

        ttk.Button(

            formulario,

            text="Registrar Venta",

            command=self.registrar

        ).grid(
            row=8,
            column=0,
            columnspan=2,
            pady=15
        )
        # ===========================
        # HISTORIAL DE VENTAS
        # ===========================

# ===========================
# HISTORIAL DE VENTAS
# ===========================

        frame_historial = tk.LabelFrame(
            self.contenedor,
            text="Historial de ventas",
            padx=10,
            pady=10
        )

        frame_historial.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        columnas = (
            "id",
            "fecha",
            "cliente",
            "producto",
            "cantidad",
            "costo",
            "precio",
            "subtotal",
            "delivery",
            "total"
        )

        nombres = {
            "id": "ID",
            "fecha": "Fecha",
            "cliente": "Cliente",
            "producto": "Producto",
            "cantidad": "Cantidad",
            "costo": "Costo",
            "precio": "Precio Venta",
            "subtotal": "Subtotal",
            "delivery": "Delivery",
            "total": "Total"
        }

# Contenedor para la tabla y los scrollbars
        frame_tabla = tk.Frame(frame_historial)
        frame_tabla.pack(fill="both", expand=True)

        self.tabla_ventas = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings"
        )

# Encabezados
        for columna in columnas:
            self.tabla_ventas.heading(columna, text=nombres[columna])

# Columnas
        self.tabla_ventas.column("id", width=60, anchor="center", stretch=False)
        self.tabla_ventas.column("fecha", width=140, anchor="center", stretch=False)
        self.tabla_ventas.column("cliente", width=160, stretch=False)
        self.tabla_ventas.column("producto", width=220, stretch=False)
        self.tabla_ventas.column("cantidad", width=80, anchor="center", stretch=False)
        self.tabla_ventas.column("costo", width=100, anchor="e", stretch=False)
        self.tabla_ventas.column("precio", width=110, anchor="e", stretch=False)
        self.tabla_ventas.column("subtotal", width=110, anchor="e", stretch=False)
        self.tabla_ventas.column("delivery", width=100, anchor="e", stretch=False)
        self.tabla_ventas.column("total", width=120, anchor="e", stretch=False)

# Scrollbars
        scrollbar_vertical = ttk.Scrollbar(
            frame_tabla,
            orient="vertical",
            command=self.tabla_ventas.yview
        )

        scrollbar_horizontal = ttk.Scrollbar(
            frame_tabla,
            orient="horizontal",
            command=self.tabla_ventas.xview
        )

        self.tabla_ventas.configure(
            yscrollcommand=scrollbar_vertical.set,
            xscrollcommand=scrollbar_horizontal.set
        )

# Layout responsive
        self.tabla_ventas.grid(row=0, column=0, sticky="nsew")
        scrollbar_vertical.grid(row=0, column=1, sticky="ns")
        scrollbar_horizontal.grid(row=1, column=0, sticky="ew")

        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)

        self.cargar_ventas()
        
    def cambiar_producto(self, event=None):

        indice = self.cmb_producto.current()

        if indice >= 0:

            producto = self.productos[indice]

            self.txt_precio.config(
                state="normal"
            )

            self.txt_precio.delete(
                0,
                tk.END
            )

            self.txt_precio.insert(
                0,
                str(producto.precio_venta)
            )

            self.txt_precio.config(
                state="readonly"
            )

            self.calcular_total()



    def calcular_total(self, event=None):

        try:

            cantidad = int(
                self.sp_cantidad.get()
            )

            precio = float(
                self.obtener_valor(
                    self.txt_precio
                )
            )


            subtotal = cantidad * precio


            delivery = 0

            if self.delivery.get():

                if self.txt_delivery.get():

                    delivery = float(
                        self.txt_delivery.get()
                    )


            total = subtotal + delivery


            self.mostrar_valor(
                self.txt_subtotal,
                subtotal
            )


            self.mostrar_valor(
                self.txt_total,
                total
            )


        except:

            pass



    def registrar(self):

        try:

            if self.cmb_producto.current() == -1:

                messagebox.showwarning(
                    "Aviso",
                    "Seleccione un producto."
                )

                return


            cliente = self.txt_cliente.get().strip()


            if cliente == "":

                messagebox.showwarning(
                    "Aviso",
                    "Ingrese el cliente."
                )

                return



            producto = self.productos[
                self.cmb_producto.current()
            ]


            cantidad = int(
                self.sp_cantidad.get()
            )


            precio = producto.precio_venta


            subtotal = cantidad * precio


            delivery = 0


            if self.delivery.get():

                delivery = float(
                    self.txt_delivery.get()
                )


            total = subtotal + delivery



            venta = Venta(

                fecha=datetime.now().strftime("%d/%m/%Y %H:%M"),

                cliente=cliente,

                producto_id=producto.id,

                producto_nombre=producto.nombre,

                cantidad=cantidad,

                costo_unitario=producto.precio_costo,

                precio_unitario=producto.precio_venta,

                subtotal=subtotal,

                delivery=delivery,

                total=total

            )


            self.venta_repository.agregar(
                venta
            )


            messagebox.showinfo(
                "Correcto",
                "Venta registrada."
            )


            self.limpiar()
            self.cargar_ventas()



        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )



    def mostrar_valor(self, campo, valor):

        campo.config(
            state="normal"
        )

        campo.delete(
            0,
            tk.END
        )

        campo.insert(
            0,
            str(round(valor,2))
        )

        campo.config(
            state="readonly"
        )



    def obtener_valor(self, campo):

        return campo.get()



    def limpiar(self):

        self.txt_cliente.delete(
            0,
            tk.END
        )

        self.cmb_producto.set(
            ""
        )

        self.sp_cantidad.delete(
            0,
            tk.END
        )

        self.sp_cantidad.insert(
            0,
            "1"
        )

        self.txt_delivery.delete(
            0,
            tk.END
        )

        self.txt_delivery.insert(
            0,
            "0"
        )


        self.delivery.set(False)


        for campo in [
            self.txt_precio,
            self.txt_subtotal,
            self.txt_total
        ]:

            campo.config(
                state="normal"
            )

            campo.delete(
                0,
                tk.END
            )

            campo.config(
                state="readonly"
            )
    def cargar_ventas(self):

        registros = self.venta_repository.listar()

        for fila in self.tabla_ventas.get_children():

            self.tabla_ventas.delete(fila)

        for venta in registros:

            self.tabla_ventas.insert(

                "",

                tk.END,

                values=(

                    venta[0],   # ID
                    venta[1],   # Fecha
                    venta[2],   # Cliente
                    venta[3],   # Producto
                    venta[4],   # Cantidad
                    venta[5],   # Costo
                    venta[6],   # Precio
                    venta[7],   # Subtotal
                    venta[8],   # Delivery
                    venta[9]    # Total

                )

    
            )