# reports/utils/pdf_utils.py

"""
Módulo para gerar relatórios em PDF para os apps do projeto.
"""

from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas as reportlab_canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
class FooterCanvas(reportlab_canvas.Canvas):
    """
    Canvas personalizado para adicionar rodapé em cada página do PDF.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_count = 0  # Contador de páginas

    def draw_footer(self, total_pages):
        """
        Desenha o rodapé na página atual.
        """
        page_text = f"Página {self._pageNumber} de {total_pages}"
        self.setFont("Helvetica", 10)
        self.drawRightString(landscape(A4)[0] - inch, 0.75 * inch, page_text)

    def showPage(self):
        """
        Incrementa o contador de páginas e desenha o rodapé antes de mudar para a próxima página.
        """
        self.page_count += 1
        super().showPage()

    def save(self):
        """
        Sobrescreve o método save para garantir que o rodapé seja desenhado em todas as páginas.
        """
        total_pages = len(self._pages) + 1
        for page in self._pages:
            self.__dict__.update(page)
            self.draw_footer(total_pages)
            super().showPage()
        super().save()

    def inkAnnotation(self, *args, **kwargs):
        """
        Implementação do método abstrato inkAnnotation.
        """

    def inkAnnotation0(self, *args, **kwargs): # pylint: disable=invalid-name
        """
        Implementação do método abstrato inkAnnotation0.
        """

def draw_header(canvas, doc, title):
    """
    Desenha o cabeçalho do relatório com fundo colorido, espaço para logo e título ajustável.
    """
    canvas.saveState()

    page_width, page_height = landscape(A4)
    header_height = 1.2 * inch
    logo_width = page_width * 0.25  # 25% da largura
    text_width = page_width * 0.75  # 75% da largura
    padding = 0.2 * inch  # Espaçamento interno

    # Fundo do cabeçalho
    canvas.setFillColor(colors.HexColor("#1a4f45"))
    canvas.rect(0, page_height - header_height, page_width, header_height, fill=True, stroke=False)

    # Espaço para a logo (comentado até ser definida)
    # logo_path = "caminho/para/sua/logo.png"
    # logo = Image(logo_path, width=logo_width - padding, height=header_height - padding)
    # logo.drawOn(canvas, padding, page_height - header_height + padding)

    # Ajuste automático do tamanho do título
    max_font_size = 22
    min_font_size = 12
    font_name = "Helvetica-Bold"  # Alternativa ao Arial Black
    text_x = logo_width + padding
    text_y = page_height - (header_height / 2)  # Centralizado verticalmente
    text_max_width = text_width - 2 * padding

    font_size = max_font_size
    while (canvas.stringWidth(title, font_name, font_size) > text_max_width and
           font_size > min_font_size):
        font_size -= 1

    canvas.setFillColor(colors.white)
    canvas.setFont(font_name, font_size)
    canvas.drawCentredString(text_x + (text_width / 2), text_y, title)

    canvas.restoreState()

def report_create_pdf(response, title, data):
    """
    Gera o relatório em PDF com cabeçalho padronizado e tabela formatada.
    """
    doc = SimpleDocTemplate(response,
                            pagesize=landscape(A4),
                            leftMargin=0.5 * inch,
                            rightMargin=0.5 * inch,
                            topMargin=1.8 * inch,
                            bottomMargin=0.5 * inch,
                            canvasmaker=FooterCanvas
                            )
    elements = []

    # Subtítulo com data de geração
    styles = getSampleStyleSheet()
    subtitle = Paragraph(
        f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        styles['Normal']
    )
    elements.append(subtitle)

    # Estilo das células da tabela
    cell_style = ParagraphStyle(name='Normal', wordWrap='CJK')
    data = [[Paragraph(str(cell), cell_style) for cell in row] for row in data]

    # Criar tabela
    col_widths = [landscape(A4)[0] / len(data[0])] * len(data[0])
    table = Table(data, colWidths=col_widths)

    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E6B510')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ])

    # Adicionar cores alternadas nas linhas
    for i in range(1, len(data)):
        bg_color = colors.HexColor('#e3e3e1') if i % 2 == 0 else colors.white
        table_style.add('BACKGROUND', (0, i), (-1, i), bg_color)

    table.setStyle(table_style)
    elements.append(table)

    # Adicionar cabeçalho nas páginas
    def on_page(c, d):
        draw_header(c, d, title)

    doc.build(elements, onFirstPage=on_page, onLaterPages=on_page)

    return response
