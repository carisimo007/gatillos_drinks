import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

from modelos.gasto import Gasto
from modelos.categoria_gasto import CategoriaGasto

from repositorios.gasto_repository import GastoRepository
from repositorios.categoria_gasto_repository import CategoriaGastoRepository
from interfaz.categorias_gasto import VentanaCategoriasGasto


class VentanaGastos:

    def __init__(self, padre):

        self.padre = padre

        self.repo_gastos = GastoRepository()
        self.repo_categorias = CategoriaGastoRepository()

        self.gasto_seleccionado = None


    def mostrar(self):

        self.frame = tk.Frame(self.padre)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        titulo = tk.Label(

            self.frame,

            text="Gestión de Gastos",

            font=("Arial", 18, "bold")

        )

        titulo.pack(pady=10)

        self.crear_formulario()

        self.crear_busqueda()

        self.crear_tabla()

        self.cargar_categorias()

        self.actualizar_tabla()
    def crear_formulario(self):

        formulario = tk.LabelFrame(

            self.frame,

            text="Nuevo Gasto"

        )

        formulario.pack(

            fill="x",

            pady=10

        )


        tk.Label(

            formulario,

            text="Descripción"

        ).grid(

            row=0,

            column=0,

            padx=5,

            pady=5,

            sticky="w"

        )


        self.entry_descripcion = tk.Entry(

            formulario,

            width=40

        )

        self.entry_descripcion.grid(

            row=0,

            column=1,

            padx=5,

            pady=5

        )


        tk.Label(

            formulario,

            text="Categoría"

        ).grid(

            row=1,

            column=0,

            padx=5,

            pady=5,

            sticky="w"

        )


        self.combo_categoria = ttk.Combobox(

            formulario,

            state="normal",

            width=30

        )
        
        self.combo_categoria.bind(
            "<KeyRelease>",
            self.filtrar_categorias
        )

        self.combo_categoria.grid(

            row=1,

            column=1,

            padx=5,

            pady=5

        )


        self.boton_nueva_categoria = ttk.Button(
            formulario,
            text="+",
            command=self.abrir_categorias
        )

        self.boton_nueva_categoria.grid(

            row=1,

            column=2,

            padx=5

        )


        tk.Label(

            formulario,

            text="Monto"

        ).grid(

            row=2,

            column=0,

            padx=5,

            pady=5,

            sticky="w"

        )


        self.entry_monto = tk.Entry(

            formulario,

            width=20

        )

        self.entry_monto.grid(

            row=2,

            column=1,

            padx=5,

            pady=5,

            sticky="w"

        )


        tk.Label(

            formulario,

            text="Fecha"

        ).grid(

            row=3,

            column=0,

            padx=5,

            pady=5,

            sticky="w"

        )


        self.entry_fecha = tk.Entry(

            formulario,

            width=20

        )

        self.entry_fecha.insert(

            0,

            datetime.now().strftime("%d/%m/%Y")

        )

        self.entry_fecha.grid(

            row=3,

            column=1,

            padx=5,

            pady=5,

            sticky="w"

        )


        self.boton_guardar = ttk.Button(
            formulario,
            text="Registrar Gasto",
            command=self.guardar_gasto
        )

        self.boton_guardar.grid(

            row=4,

            column=0,

            columnspan=3,

            pady=15

        )
    def crear_busqueda(self):

        marco = tk.Frame(
            self.frame
        )

        marco.pack(
            fill="x",
            pady=10
        )


        tk.Label(
            marco,
            text="Buscar:"
        ).pack(
            side="left",
            padx=5
        )


        self.entry_buscar = tk.Entry(
            marco,
            width=40
        )

        self.entry_buscar.pack(
            side="left",
            padx=5
        )


        boton_buscar = ttk.Button(
            marco,
            text="Buscar",
            command=self.buscar
        )

        boton_buscar.pack(
            side="left",
            padx=5
        )
    def crear_tabla(self):

        columnas = (

            "id",
            "fecha",
            "categoria",
            "descripcion",
            "monto"

        )


        self.tabla = ttk.Treeview(
        
            self.frame,

           columns=columnas,

            show="headings"

        )
        self.tabla.bind(
            "<Button-1>",
            self.ordenar_tabla
        )


        self.tabla.heading(
            "id",
            text="ID"
        )

        self.tabla.heading(
            "fecha",
            text="Fecha"
        )

        self.tabla.heading(
            "categoria",
            text="Categoría"
        )

        self.tabla.heading(
            "descripcion",
            text="Descripción"
        )

        self.tabla.heading(
            "monto",
            text="Monto"
        )


        self.tabla.column(
            "id",
            width=50
        )

        self.tabla.column(
            "fecha",
            width=100
        )

        self.tabla.column(
            "categoria",
            width=150
        )

        self.tabla.column(
            "descripcion",
            width=300
        )

        self.tabla.column(
            "monto",
            width=100
        )


        self.tabla.pack(
            fill="both",
            expand=True
        )
        botones = tk.Frame(
            self.frame
        )

        botones.pack(
        pady=10
        )


        boton_editar = ttk.Button(
            botones,
            text="✏️ Editar",
            command=self.editar_gasto
        )

        boton_editar.pack(
            side="left",
            padx=10
        )


        boton_eliminar = ttk.Button(
            botones,
            text="🗑️ Eliminar",
            command=self.eliminar_gasto
        )

        boton_eliminar.pack(
            side="left",
            padx=10
        )

    def ordenar_tabla(self, evento):

        region = self.tabla.identify_region(
            evento.x,
            evento.y
        )

        if region != "heading":

            return


        columna = self.tabla.identify_column(
            evento.x
        )


        datos = []

        for fila in self.tabla.get_children():

            valores = self.tabla.item(fila)["values"]

            datos.append(valores)


        indice = int(
            columna.replace("#","")
        ) - 1


        datos.sort(

            key=lambda x: x[indice]

        )


        for fila in self.tabla.get_children():

            self.tabla.delete(fila)


        for dato in datos:

            self.tabla.insert(
                "",
                "end",
                values=dato
            )

    def seleccionar_gasto(self):

        seleccionado = self.tabla.selection()


        if not seleccionado:

            return None


        valores = self.tabla.item(
            seleccionado[0]
        )["values"]


        return valores[0]
    
    def editar_gasto(self):

        id_gasto = self.seleccionar_gasto()


        if not id_gasto:

            messagebox.showwarning(
                "Aviso",
                "Seleccione un gasto"
            )

            return


        gasto = self.repo_gastos.obtener_por_id(
            id_gasto
        )


        self.entry_descripcion.delete(
            0,
            tk.END
        )

        self.entry_descripcion.insert(
            0,
            gasto.descripcion
        )


        self.entry_monto.delete(
            0,
            tk.END
        )

        self.entry_monto.insert(
            0,
            gasto.monto
        )


        self.entry_fecha.delete(
            0,
            tk.END
        )

        self.entry_fecha.insert(
            0,
            gasto.fecha
        )


        self.gasto_seleccionado = gasto
        
    def actualizar_tabla(self):

        for fila in self.tabla.get_children():

            self.tabla.delete(fila)


        gastos = self.repo_gastos.listar()


        for gasto in gastos:

            self.tabla.insert(

                "",

                "end",

                values=gasto

            )
    def buscar(self):

        texto = self.entry_buscar.get()


        for fila in self.tabla.get_children():

            self.tabla.delete(fila)


        gastos = self.repo_gastos.buscar(
            texto
        )


        for gasto in gastos:

            self.tabla.insert(

                "",

                "end",

                values=gasto

            )
    def cargar_categorias(self):

        categorias = self.repo_categorias.listar()

        self.categorias = {}

        valores = []


        for categoria in categorias:

            self.categorias[categoria.nombre] = categoria.id

            valores.append(
                categoria.nombre
            )


        # ordenar alfabéticamente

        valores.sort(
            key=str.lower
        )


        self.combo_categoria["values"] = valores


        if valores:

            self.combo_categoria.current(0)
    def guardar_gasto(self):

        descripcion = self.entry_descripcion.get()

        categoria_nombre = self.combo_categoria.get()

        monto = self.entry_monto.get()

        fecha = self.entry_fecha.get()


        if descripcion == "" or categoria_nombre == "" or monto == "":

            messagebox.showwarning(
                "Datos incompletos",
                "Complete todos los campos"
            )

            return


        try:

            monto = float(monto)

        except:

            messagebox.showerror(
                "Error",
                "El monto debe ser un número"
            )

            return


        if categoria_nombre in self.categorias:

            categoria_id = self.categorias[categoria_nombre]


        else:

            crear = messagebox.askyesno(

                "Categoría nueva",

                f"La categoría '{categoria_nombre}' no existe.\n\n¿Desea crearla?"

            )


            if crear:

                nueva = CategoriaGasto(

                    nombre=categoria_nombre,

                    tipo="Operativo"

                )


                self.repo_categorias.agregar(
                   nueva
                )


                self.cargar_categorias()


                categoria_id = self.categorias[categoria_nombre]


            else:

                return


        gasto = Gasto(

            fecha=fecha,

            descripcion=descripcion,

            categoria_id=categoria_id,

            monto=monto

        )


        if self.gasto_seleccionado:

            gasto.id = self.gasto_seleccionado.id

            self.repo_gastos.actualizar(
                gasto
            )

            self.gasto_seleccionado = None


        else:

            self.repo_gastos.agregar(
                gasto
            )


        messagebox.showinfo(
            "Éxito",
            "Gasto registrado correctamente"
        )


        self.entry_descripcion.delete(
            0,
            tk.END
        )

        self.entry_monto.delete(
            0,
            tk.END
        )


        self.actualizar_tabla()
    def eliminar_gasto(self):

        id_gasto = self.seleccionar_gasto()


        if not id_gasto:

            messagebox.showwarning(
                "Aviso",
                "Seleccione un gasto"
            )

            return


        confirmar = messagebox.askyesno(

           "Eliminar",

            "¿Desea eliminar este gasto?"

        )


        if confirmar:

            self.repo_gastos.eliminar(
                id_gasto
            )


            self.actualizar_tabla()
    def abrir_categorias(self):

        VentanaCategoriasGasto(

            self.frame,

            self.cargar_categorias

        )
    def filtrar_categorias(self, evento):

        texto = self.combo_categoria.get()


        if texto == "":

            self.combo_categoria["values"] = sorted(
                self.categorias.keys(),
                key=str.lower
            )

            return


        coincidencias = []


        for categoria in self.categorias.keys():

            if texto.lower() in categoria.lower():

                coincidencias.append(
                    categoria
                )


        self.combo_categoria["values"] = sorted(
            coincidencias,
            key=str.lower
        )