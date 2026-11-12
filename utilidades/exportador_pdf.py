from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

from datetime import datetime


class ExportadorPDF:

    def __init__(self):

        self.margen = 45

        self.ancho, self.alto = A4

        self.y = 0

    # =====================================================
    # MÉTODO PRINCIPAL
    # =====================================================

    def exportar_caja(

        self,

        movimientos,

        fecha_desde,

        fecha_hasta,

        archivo

    ):

        pdf = canvas.Canvas(

            archivo,

            pagesize=A4

        )

        self.y = self.alto - 50

        self._encabezado(

            pdf,

            fecha_desde,

            fecha_hasta

        )

        self._encabezados(pdf)

        self._movimientos(

            pdf,

            movimientos

        )

        self._resumen(

            pdf,

            movimientos

        )

        self._pie(pdf)

        pdf.save()

    # =====================================================
    # ESCRIBIR TEXTO
    # =====================================================

    def escribir(

        self,

        pdf,

        texto,

        x,

        tamaño=10,

        fuente="Helvetica",

        color=colors.black

    ):

        pdf.setFont(

            fuente,

            tamaño

        )

        pdf.setFillColor(

            color

        )

        pdf.drawString(

            x,

            self.y,

            str(texto)

        )

    # =====================================================
    # SALTO
    # =====================================================

    def salto(

        self,

        pixeles

    ):

        self.y -= pixeles

    # =====================================================
    # LÍNEA
    # =====================================================

    def linea(

        self,

        pdf

    ):

        pdf.setStrokeColor(

            colors.lightgrey

        )

        pdf.line(

            self.margen,

            self.y,

            self.ancho - self.margen,

            self.y

        )
# =====================================================
# ENCABEZADO
# =====================================================

    def _encabezado(

        self,

        pdf,

        fecha_desde,

        fecha_hasta

    ):

        # Título principal
        self.escribir(

            pdf,

            "GATILLOS DRINKS",

            self.margen,

            tamaño=22,

            fuente="Helvetica-Bold"

        )

        self.salto(28)

    # Subtítulo
        self.escribir(

            pdf,

            "Libro de Caja",

            self.margen,

            tamaño=12,

            fuente="Helvetica"

        )

    # Fecha de generación (arriba a la derecha)
        pdf.setFont(

            "Helvetica",

            9

        )

        pdf.setFillColor(

            colors.grey

        )

        pdf.drawRightString(

            self.ancho - self.margen,

            self.alto - 45,

            "Generado"

        )

        pdf.drawRightString(

            self.ancho - self.margen,

            self.alto - 58,

            datetime.now().strftime("%d/%m/%Y %H:%M")

        )

        self.salto(22)

    # Período
        self.escribir(

            pdf,

            f"Período: {fecha_desde}  -  {fecha_hasta}",

            self.margen,

            tamaño=11

        )

        self.salto(18)

    # Línea separadora
        self.linea(pdf)

        self.salto(18)
        
    def _encabezados(self, pdf):

        pdf.setFillColor(colors.HexColor("#F2F2F2"))

        pdf.rect(

            self.margen,

            self.y - 5,

            self.ancho - (self.margen * 2),

            22,

            fill=1,

            stroke=0

        )

        pdf.setFillColor(colors.black)

        pdf.setFont(

            "Helvetica-Bold",

            10

        )

        pdf.drawString(50, self.y, "●")

        pdf.drawString(70, self.y, "Fecha")

        pdf.drawString(145, self.y, "Movimiento")

        pdf.drawString(250, self.y, "Cliente")

        pdf.drawString(390, self.y, "Detalle")

        pdf.drawRightString(

            self.ancho - 50,

            self.y,

            "Monto"

        )

        self.salto(25)

    def _movimientos(

        self,

        pdf,

        movimientos

    ):

        verde = colors.HexColor("#2E7D32")

        rojo = colors.HexColor("#C62828")

        total_ingresos = 0

        total_gastos = 0

        for movimiento in movimientos:

            fecha = movimiento[0]

            tipo = movimiento[1]

            cliente = movimiento[2]

            detalle = movimiento[3]

            monto = movimiento[4]

            if tipo == "INGRESO":

                color = verde

                punto = "●"

                texto = "Ingreso"

                total_ingresos += monto

            else:

                color = rojo

                punto = "●"

                texto = "Gasto"

                total_gastos += monto

            pdf.setFont(

                "Helvetica",

                10

            )

            pdf.setFillColor(color)

            pdf.drawString(50, self.y, punto)

            pdf.drawString(145, self.y, texto)

            pdf.drawRightString(

                self.ancho - 50,

                self.y,

                f"$ {monto:,.2f}"

            )

            pdf.setFillColor(colors.black)

            pdf.drawString(70, self.y, fecha)

            pdf.drawString(250, self.y, cliente)

            pdf.drawString(390, self.y, detalle)

            self.salto(18)

        self.total_ingresos = total_ingresos

        self.total_gastos = total_gastos


    def _resumen(self, pdf, movimientos):
        pass


    def _pie(self, pdf):
        pass