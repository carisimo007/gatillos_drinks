import tkinter as tk
from tkinter import ttk, messagebox

from modelos.producto import Producto
from repositorios.producto_repository import ProductoRepository


class VentanaProductos:

    def __init__(self, contenedor):

        self.contenedor = contenedor

        self.repository = ProductoRepository()

        self.id_producto = None

        self.orden_inverso = False


    def mostrar(self):

        for widget in self.contenedor.winfo_children():
            widget.destroy()

        titulo = tk.Label(
            self.contenedor,
            text="Gestión de Productos",
            font=("Arial", 18, "bold")
        )

        titulo.pack(pady=10)


        # ===========================
        # BUSCADOR
        # ===========================

        frame_busqueda = tk.Frame(self.contenedor)
        frame_busqueda.pack(fill="x", padx=15)

        tk.Label(
            frame_busqueda,
            text="Buscar:"
        ).pack(side="left")

        self.txt_buscar = tk.Entry(
            frame_busqueda,
            width=40
        )

        self.txt_buscar.pack(
            side="left",
            padx=5
        )

        self.txt_buscar.bind(
            "<KeyRelease>",
            self.buscar
        )

        ttk.Button(
            frame_busqueda,
            text="Mostrar todos",
            command=self.cargar_productos
        ).pack(
            side="left",
            padx=5
        )


        # ===========================
        # FORMULARIO
        # ===========================

        formulario = tk.LabelFrame(
            self.contenedor,
            text="Datos del producto",
            padx=10,
            pady=10
        )

        formulario.pack(
            fill="x",
            padx=15,
            pady=10
        )


        tk.Label(formulario,text="Nombre").grid(row=0,column=0,padx=5,pady=5,sticky="w")

        self.txt_nombre = tk.Entry(formulario,width=40)
        self.txt_nombre.grid(row=0,column=1,padx=5,pady=5)



        tk.Label(formulario,text="Categoría").grid(row=1,column=0,padx=5,pady=5,sticky="w")

        self.txt_categoria = tk.Entry(formulario,width=40)
        self.txt_categoria.grid(row=1,column=1,padx=5,pady=5)



        tk.Label(formulario,text="Precio costo").grid(row=2,column=0,padx=5,pady=5,sticky="w")

        self.txt_costo = tk.Entry(formulario,width=20)
        self.txt_costo.grid(row=2,column=1,sticky="w",padx=5,pady=5)



        tk.Label(formulario,text="Precio sugerido").grid(row=3,column=0,padx=5,pady=5,sticky="w")

        self.txt_sugerido = tk.Entry(
            formulario,
            width=20,
            state="readonly"
        )

        self.txt_sugerido.grid(
            row=3,
            column=1,
            sticky="w",
            padx=5,
            pady=5
        )



        tk.Label(formulario,text="Precio venta").grid(row=4,column=0,padx=5,pady=5,sticky="w")

        self.txt_venta = tk.Entry(
            formulario,
            width=20
        )

        self.txt_venta.grid(
            row=4,
            column=1,
            sticky="w",
            padx=5,
            pady=5
        )


        self.txt_costo.bind(
            "<KeyRelease>",
            self.calcular_sugerido
        )


        # ===========================
        # BOTONES
        # ===========================

        frame_botones = tk.Frame(formulario)
        frame_botones.grid(
            row=5,
            column=0,
            columnspan=2,
            pady=10
        )



        ttk.Button(
            frame_botones,
            text="Nuevo",
            width=12,
            command=self.nuevo
        ).pack(side="left",padx=5)



        ttk.Button(
            frame_botones,
            text="Guardar",
            width=12,
            command=self.guardar
        ).pack(side="left",padx=5)



        ttk.Button(
            frame_botones,
            text="Modificar",
            width=12,
            command=self.modificar
        ).pack(side="left",padx=5)



        ttk.Button(
            frame_botones,
            text="Eliminar",
            width=12,
            command=self.eliminar
        ).pack(side="left",padx=5)



        # ===========================
        # TABLA
        # ===========================

        frame_tabla = tk.Frame(self.contenedor)
        frame_tabla.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )



        columnas = (
            "id",
            "nombre",
            "categoria",
            "costo",
            "sugerido",
            "venta",
            "ganancia"
        )


        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings"
        )



        self.tabla.heading("id",text="ID",command=lambda:self.ordenar("id"))
        self.tabla.heading("nombre",text="Nombre",command=lambda:self.ordenar("nombre"))
        self.tabla.heading("categoria",text="Categoría",command=lambda:self.ordenar("categoria"))
        self.tabla.heading("costo",text="Costo",command=lambda:self.ordenar("costo"))
        self.tabla.heading("sugerido",text="Sugerido",command=lambda:self.ordenar("sugerido"))
        self.tabla.heading("venta",text="Venta",command=lambda:self.ordenar("venta"))
        self.tabla.heading("ganancia",text="Ganancia",command=lambda:self.ordenar("ganancia"))



        self.tabla.column("id",width=60,anchor="center")
        self.tabla.column("nombre",width=220)
        self.tabla.column("categoria",width=150)
        self.tabla.column("costo",width=100,anchor="e")
        self.tabla.column("sugerido",width=100,anchor="e")
        self.tabla.column("venta",width=100,anchor="e")
        self.tabla.column("ganancia",width=100,anchor="e")



        scrollbar = ttk.Scrollbar(
            frame_tabla,
            orient="vertical",
            command=self.tabla.yview
        )

        self.tabla.configure(
            yscrollcommand=scrollbar.set
        )



        self.tabla.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )



        self.tabla.bind(
            "<<TreeviewSelect>>",
            self.seleccionar_producto
        )



        self.tabla.bind(
            "<Double-1>",
            self.seleccionar_producto
        )



        self.cargar_productos()
    def nuevo(self):

        self.id_producto = None

        self.txt_nombre.delete(0, tk.END)
        self.txt_categoria.delete(0, tk.END)
        self.txt_costo.delete(0, tk.END)
        self.txt_venta.delete(0, tk.END)

        self.txt_sugerido.config(state="normal")
        self.txt_sugerido.delete(0, tk.END)
        self.txt_sugerido.config(state="readonly")

        self.txt_nombre.focus()


    def calcular_sugerido(self, event=None):

        try:

            costo = float(self.txt_costo.get().replace(",", "."))

            sugerido = round(costo * 1.30, 2)

            self.txt_sugerido.config(state="normal")
            self.txt_sugerido.delete(0, tk.END)
            self.txt_sugerido.insert(0, str(sugerido))
            self.txt_sugerido.config(state="readonly")

        except:

            self.txt_sugerido.config(state="normal")
            self.txt_sugerido.delete(0, tk.END)
            self.txt_sugerido.config(state="readonly")


    def guardar(self):

        try:

            producto = Producto(

                nombre=self.txt_nombre.get().strip(),
                categoria=self.txt_categoria.get().strip(),
                precio_costo=float(self.txt_costo.get()),
                precio_venta=float(self.txt_venta.get())

            )

            self.repository.agregar(producto)

            messagebox.showinfo(
                "Correcto",
                "Producto guardado."
            )

            self.nuevo()

            self.cargar_productos()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )


    def modificar(self):

        if self.id_producto is None:

            messagebox.showwarning(
                "Aviso",
                "Seleccione un producto."
            )

            return

        try:

            producto = Producto(

                id=self.id_producto,

                nombre=self.txt_nombre.get(),

                categoria=self.txt_categoria.get(),

                precio_costo=float(self.txt_costo.get()),

                precio_venta=float(self.txt_venta.get())

            )

            self.repository.actualizar(producto)

            messagebox.showinfo(
                "Correcto",
                "Producto actualizado."
            )

            self.nuevo()

            self.cargar_productos()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )


    def eliminar(self):

        if self.id_producto is None:

            messagebox.showwarning(
                "Aviso",
                "Seleccione un producto."
            )

            return

        respuesta = messagebox.askyesno(

            "Eliminar",

            "¿Desea eliminar el producto?"

        )

        if not respuesta:

            return

        self.repository.eliminar(
            self.id_producto
        )

        self.nuevo()

        self.cargar_productos()


    def cargar_productos(self):

        productos = self.repository.listar()

        self.mostrar_productos(productos)


    def buscar(self, event=None):

        texto = self.txt_buscar.get()

        productos = self.repository.buscar(texto)

        self.mostrar_productos(productos)


    def mostrar_productos(self, productos):

        for fila in self.tabla.get_children():

            self.tabla.delete(fila)

        for producto in productos:

            self.tabla.insert(

                "",

                tk.END,

                values=(

                    producto.id,

                    producto.nombre,

                    producto.categoria,

                    producto.precio_costo,

                    producto.precio_sugerido,

                    producto.precio_venta,

                    producto.ganancia

                )

            )


    def seleccionar_producto(self, event=None):

        seleccion = self.tabla.selection()

        if not seleccion:

            return

        valores = self.tabla.item(
            seleccion[0]
        )["values"]

        self.id_producto = valores[0]

        self.nuevo()

        self.id_producto = valores[0]

        self.txt_nombre.insert(
            0,
            valores[1]
        )

        self.txt_categoria.insert(
            0,
            valores[2]
        )

        self.txt_costo.insert(
            0,
            valores[3]
        )

        self.calcular_sugerido()

        self.txt_venta.insert(
            0,
            valores[5]
        )


    def ordenar(self, columna):

        datos = [

            (

                self.tabla.set(item, columna),

                item

            )

            for item in self.tabla.get_children()

        ]

        datos    
    def ordenar(self, columna):

        datos = []

        for item in self.tabla.get_children():

            valor = self.tabla.set(item, columna)

            try:
                valor = float(valor)
            except:
                pass

            datos.append((valor, item))

        datos.sort(reverse=self.orden_inverso)

        self.orden_inverso = not self.orden_inverso

        for indice, (_, item) in enumerate(datos):

            self.tabla.move(
                item,
                "",
                indice
            )  