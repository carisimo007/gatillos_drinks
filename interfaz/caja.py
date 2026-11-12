import tkinter as tk
from tkinter import ttk
from datetime import datetime

from repositorios.caja_repository import CajaRepository
from utilidades.exportador_pdf_viejo import ExportadorPDF
from tkinter import filedialog, messagebox


class VentanaCaja:


    def __init__(self, padre):

        self.padre = padre

        self.repo = CajaRepository()

        self.exportador = ExportadorPDF()

    def mostrar(self):

        self.frame = tk.Frame(
            self.padre
        )

        self.frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )


        titulo = tk.Label(

            self.frame,

            text="Libro de Caja",

            font=("Arial", 20, "bold")

        )

        titulo.pack(
            pady=10
        )


        self.crear_filtros()

        self.crear_tabla()

        self.crear_resumen()

        self.cargar_movimientos()



    def crear_filtros(self):

        marco = tk.Frame(
            self.frame
        )

        marco.pack(
            fill="x",
            pady=10
        )


        tk.Label(

            marco,

            text="Desde"

        ).pack(
            side="left",
            padx=5
        )


        self.fecha_desde = tk.Entry(
            marco,
            width=12
        )

        self.fecha_desde.insert(

            0,

            datetime.now().strftime("%d/%m/%Y")

        )

        self.fecha_desde.pack(
            side="left",
            padx=5
        )


        tk.Label(

            marco,

            text="Hasta"

        ).pack(
            side="left",
            padx=5
        )


        self.fecha_hasta = tk.Entry(
            marco,
            width=12
        )

        self.fecha_hasta.insert(

            0,

            datetime.now().strftime("%d/%m/%Y")

        )

        self.fecha_hasta.pack(
            side="left",
            padx=5
        )


        boton = ttk.Button(

            marco,

            text="Consultar",

            command=self.cargar_movimientos

        )

        boton.pack(
            side="left",
            padx=10
        )

        boton_pdf = ttk.Button(

            marco,

            text="📄 Exportar PDF",

            command=self.exportar_pdf

        )

        boton_pdf.pack(

            side="left",

            padx=10

        )

    def crear_tabla(self):

        columnas = (

            "estado",

            "fecha",

            "movimiento",

            "cliente",

            "detalle",

            "monto"

        )
        self.tabla = ttk.Treeview(

            self.frame,

            columns=columnas,

            show="headings"

        )
        
        self.tabla.tag_configure(

            "ingreso",

            foreground="#198754"

        )

        self.tabla.tag_configure(

            "gasto",

            foreground="#dc3545"

        )


        self.tabla.heading(
            "estado",
            text=""
        )

        self.tabla.heading(
            "fecha",
            text="Fecha"
        )

        self.tabla.heading(
            "movimiento",
            text="Movimiento"
        )

        self.tabla.heading(
            "cliente",
            text="Cliente"
        )

        self.tabla.heading(
            "detalle",
            text="Detalle"
        )

        self.tabla.heading(
            "monto",
            text="Monto"
        )

        self.tabla.column(
            "estado",
            width=35,
            anchor="center",
            stretch=False
        )

        self.tabla.column(
            "fecha",
            width=120,
            anchor="center"
        )

        self.tabla.column(
            "movimiento",
            width=100,
            anchor="center"
        )

        self.tabla.column(
            "cliente",
            width=170
        )

        self.tabla.column(
            "detalle",
            width=320
        )

        self.tabla.column(
            "monto",
            width=120,
            anchor="e"
        )


        self.tabla.pack(

            fill="both",

            expand=True

        )



    def crear_resumen(self):

        marco = tk.Frame(
            self.frame
        )

        marco.pack(
            pady=15
        )


        self.lbl_ingresos = tk.Label(

            marco,

            text="Ingresos: $0",

            font=("Arial",14,"bold")

        )

        self.lbl_ingresos.pack(
            side="left",
            padx=30
        )


        self.lbl_gastos = tk.Label(

            marco,

            text="Gastos: $0",

            font=("Arial",14,"bold")

        )

        self.lbl_gastos.pack(
            side="left",
            padx=30
        )


        self.lbl_saldo = tk.Label(

            marco,

            text="Saldo: $0",

            font=("Arial",14,"bold")

        )

        self.lbl_saldo.pack(
            side="left",
            padx=30
        )
    def cargar_movimientos(self):

        # limpiar tabla

        for fila in self.tabla.get_children():

            self.tabla.delete(fila)


        fecha_desde = self.fecha_desde.get()

        fecha_hasta = self.fecha_hasta.get()


        movimientos = self.repo.listar(

            fecha_desde,

            fecha_hasta

        )

        self.movimientos = movimientos

        total_ingresos = 0

        total_gastos = 0


        for movimiento in movimientos:

            fecha = movimiento[0]

            tipo = movimiento[1]

            cliente = movimiento[2]

            concepto = movimiento[3]

            monto = movimiento[4]


            if tipo == "INGRESO":

                estado = "🟢"
                
                movimiento = "Ingreso"

                tag = "ingreso"

                total_ingresos += monto

            else:

                estado = "🔴"
                
                movimiento ="Gasto"

                tag = "gasto"

                total_gastos += monto


            self.tabla.insert(

                "",

                "end",

                values=(

                    estado,

                    fecha,
                    
                    movimiento,

                    cliente,

                    concepto,

                    f"$ {monto:,.2f}"

                ),

                tags=(tag,)

            )



        saldo = total_ingresos - total_gastos


        self.lbl_ingresos.config(

            text=f"Ingresos: ${total_ingresos:,.2f}"

        )


        self.lbl_gastos.config(

            text=f"Gastos: ${total_gastos:,.2f}"

        )


        self.lbl_saldo.config(

            text=f"Saldo: ${saldo:,.2f}"

        )
    def exportar_pdf(self):

        archivo = filedialog.asksaveasfilename(

            title="Guardar Libro de Caja",

            defaultextension=".pdf",

            filetypes=[

                ("Archivo PDF", "*.pdf")

            ],

            initialfile="Libro_Caja.pdf"

        )

        if not archivo:

            return

        self.exportador.exportar_caja(

            self.movimientos,

            self.fecha_desde.get(),

            self.fecha_hasta.get(),

            archivo

        )

        messagebox.showinfo(

            "PDF generado",

            "El libro de caja fue exportado correctamente."

        )