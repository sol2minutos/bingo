import random
from fpdf import FPDF
from tkinter import Tk, filedialog
import os

# Función para generar una carta de bingo
def generar_carta_bingo(serie):
    carta = {
        "B": random.sample(range(1, 16), 5),
        "I": random.sample(range(16, 31), 5),
        "N": random.sample(range(31, 46), 5),
        "G": random.sample(range(46, 61), 5),
        "O": random.sample(range(61, 76), 5),
    }
    carta["N"][2] = f"{serie:03}"  # Número de serie en el espacio libre
    return carta

# Clase personalizada para el PDF
class BingoPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "", align="C", ln=True)



# Función para dibujar una carta de bingo
def dibujar_carta(pdf, carta, x_offset, y_offset, recuadro_size):
    cell_size = recuadro_size / 5  # Tamaño de cada celda
    header_height = cell_size  # Altura del encabezado personalizado
    margin = 5  # Margen negro externo (en mm, equivalente a 0.5 cm)

    # Dibujar margen negro alrededor de la carta
    pdf.set_draw_color(0, 0, 0)
    pdf.rect(x_offset - margin, y_offset - margin, recuadro_size + 2 * margin, recuadro_size + header_height + cell_size + 2 * margin, style="D")

    # Dibujar el recuadro principal
    pdf.set_line_width(0.0)
    pdf.set_draw_color(255, 255, 255)  # Cambiar el color del borde a negro
    pdf.rect(x_offset, y_offset, recuadro_size, recuadro_size + header_height + cell_size)

    # Dibujar encabezado personalizado
    pdf.set_font("Arial", "", 10)
    pdf.set_xy(x_offset, y_offset)
    pdf.multi_cell(recuadro_size, header_height / 3, "", border=0, align="L")
    pdf.multi_cell(recuadro_size, header_height / 3, "", border=0, align="L")
    pdf.multi_cell(recuadro_size, header_height / 3, "", border=0, align="L")
    pdf.multi_cell(recuadro_size, header_height / 3, "", border=0, align="L")

    # Dibujar encabezado de la tabla (BINGO)
    pdf.set_font("Arial", "B", 30)
    pdf.set_fill_color(255, 255, 255)
    pdf.set_xy(x_offset, y_offset + header_height)
    pdf.cell(recuadro_size, cell_size, " B   I    N   G    O", border=1, align="C", fill=True)

    # Dibujar los números
    pdf.set_font("Arial", "", 16)
    for fila in range(5):
        for col_idx, col in enumerate(["B", "I", "N", "G", "O"]):
            valor = carta[col][fila]
            x = x_offset + col_idx * cell_size
            y = y_offset + header_height + cell_size + fila * cell_size
            pdf.set_xy(x, y)
            pdf.set_text_color(255, 0, 0) if isinstance(valor, str) else pdf.set_text_color(0, 0, 0)
            pdf.cell(cell_size, cell_size, str(valor), border=0, align="C")  # bordeceldasblanco es en 0

# Función para crear el PDF
def crear_pdf_cartas(cantidad_cartas, nombre_archivo, imagen_fondo=None):
    pdf = BingoPDF(orientation="P", unit="mm", format="Letter")
    recuadro_size = 85  # Tamaño total del recuadro de la carta (incluido encabezado)
    x_offsets = [12, 108]  # Coordenadas horizontales ajustadas
    y_offsets = [12, 140]  # Coordenadas verticales ajustadas

    for i in range(cantidad_cartas):
        if i % 4 == 0:
            pdf.add_page()
            if imagen_fondo:
                pdf.image(imagen_fondo, x=0, y=0, w=210, h=297)

        x = x_offsets[i % 2]
        y = y_offsets[(i // 2) % 2]
        carta = generar_carta_bingo(i + 1)
        dibujar_carta(pdf, carta, x, y, recuadro_size)

    pdf.output(nombre_archivo)

# Función para seleccionar la imagen de fondo
def seleccionar_imagen_fondo():
    root = Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Selecciona una imagen de fondo",
        filetypes=[("Archivos de Imagen", "*.jpg *.jpeg *.png")]
    )

# Función para abrir el archivo PDF generado
def abrir_pdf(nombre_archivo):
    if os.name == 'nt':
        os.startfile(nombre_archivo)
    elif os.name == 'posix':
        os.system(f'open "{nombre_archivo}"')

# Flujo principal
if __name__ == "__main__":
    imagen_fondo = seleccionar_imagen_fondo()
    pdf_nombre = "bingo.pdf"

    if imagen_fondo:
        crear_pdf_cartas(100, pdf_nombre, imagen_fondo)
    else:
        crear_pdf_cartas(100, pdf_nombre)

    print(f"PDF generado: {pdf_nombre}")
    abrir_pdf(pdf_nombre)
