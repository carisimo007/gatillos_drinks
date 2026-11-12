import tkinter as tk
from tkinter import ttk, messagebox

from modelos.categoria_gasto import CategoriaGasto
from repositorios.categoria_gasto_repository import CategoriaGastoRepository


class VentanaCategoriasGasto:


    def __init__(self, padre, callback):

        self.ventana = tk.Toplevel(padre)

        self.ventana.title(
            "Categorías de Gastos"
        )

        self.ventana.geometry(
            "350x250"
        )

        self.callback = callback

        self.repo = CategoriaGastoRepository()


        self.crear_interfaz()



    def crear_interfaz(self):

        titulo = tk.Label(
            self.ventana,
            text="Nueva Categoría",
            font=("Arial",16,"bold")
        )

        titulo.pack(
            pady=15
        )


        tk.Label(
            self.ventana,
            text="Nombre"
        ).pack()


        self.entry_nombre = tk.Entry(
            self.ventana,
            width=30
        )

        self.entry_nombre.pack(
            pady=5
        )


        tk.Label(
            self.ventana,
            text="Tipo"
        ).pack()


        self.combo_tipo = ttk.Combobox(

            self.ventana,

            state="readonly",

            values=[

                "Compra",

                "Operativo"

            ]

        )

        self.combo_tipo.current(0)

        self.combo_tipo.pack(
            pady=5
        )


        boton = ttk.Button(

            self.ventana,

            text="Guardar",

            command=self.guardar

        )

        boton.pack(
            pady=15
        )



    def guardar(self):

        nombre = self.entry_nombre.get()

        tipo = self.combo_tipo.get()


        if nombre == "":

            messagebox.showwarning(

                "Aviso",

                "Ingrese un nombre"

            )

            return



        categoria = CategoriaGasto(

            nombre=nombre,

            tipo=tipo

        )


        self.repo.agregar(
            categoria
        )


        messagebox.showinfo(

            "Correcto",

            "Categoría agregada"

        )


        self.callback()


        self.ventana.destroy()