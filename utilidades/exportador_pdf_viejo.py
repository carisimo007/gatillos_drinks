from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

from datetime import datetime


class ExportadorPDF:

    def __init__(self):

        self.styles = getSampleStyleSheet()


    def exportar_caja(

        self,

        movimientos,

        fecha_desde,

        fecha_hasta,

        archivo="Libro_Caja.pdf"

    ):

        pdf = SimpleDocTemplate(

            archivo,

            pagesize=A4

        )

        elementos = []

        elementos.append(

            Paragraph(

                "<b><font size=16>GATILLOS DRINKS</font></b>",

                self.styles["Title"]

            )

        )

        elementos.append(

            Paragraph(

                "<b>LIBRO DE CAJA</b>",

                self.styles["Heading2"]

            )

        )

        elementos.append(

            Paragraph(

                f"Desde: {fecha_desde}",

                self.styles["Normal"]

            )

        )

        elementos.append(

            Paragraph(

                f"Hasta: {fecha_hasta}",

                self.styles["Normal"]

            )

        )

        elementos.append(

            Paragraph(

                "<br/>",

                self.styles["Normal"]

            )

        )

        datos = [

            [

                "Fecha",

                "Tipo",

                "Cliente",

                "Concepto",

                "Monto"

            ]

        ]

        total_ingresos = 0
        total_gastos = 0

        for movimiento in movimientos:

            fecha = movimiento[0]
            tipo = movimiento[1]
            cliente = movimiento[2]
            concepto = movimiento[3]
            monto = movimiento[4]

            if tipo == "INGRESO":

                total_ingresos += monto

                tipo_pdf = "🟢"

            else:

                total_gastos += monto

                tipo_pdf = "🔴"

            datos.append(

                [

                    fecha,

                    tipo_pdf,

                    cliente,

                    concepto,

                    f"$ {monto:,.2f}"

                ]

            )

        tabla = Table(datos)

        tabla.setStyle(

            TableStyle(

                [

                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),

                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                    ("GRID", (0, 0), (-1, -1), 1, colors.black),

                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

                    ("ALIGN", (4, 1), (4, -1), "RIGHT"),

                    ("BOTTOMPADDING", (0, 0), (-1, 0), 8)

                ]

            )

        )

        elementos.append(tabla)

        elementos.append(

            Paragraph(

                "<br/>",

                self.styles["Normal"]

            )

        )

        elementos.append(

            Paragraph(

                f"<b>Total ingresos:</b> $ {total_ingresos:,.2f}",

                self.styles["Normal"]

            )

        )

        elementos.append(

            Paragraph(

                f"<b>Total gastos:</b> $ {total_gastos:,.2f}",

                self.styles["Normal"]

            )

        )

        elementos.append(

            Paragraph(

                f"<b>Saldo:</b> $ {total_ingresos-total_gastos:,.2f}",

                self.styles["Heading2"]

            )

        )

        elementos.append(

            Paragraph(

                "<br/>",

                self.styles["Normal"]

            )

        )

        elementos.append(

            Paragraph(

                "Generado el "

                + datetime.now().strftime("%d/%m/%Y %H:%M"),

                self.styles["Italic"]

            )

        )

        pdf.build(elementos)