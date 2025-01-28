# reports/utils/pdf_utils.py

from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from datetime import datetime

class FooterCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_footer(page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_footer(self, page_count):
        page = "Página %s de %s" % (self._pageNumber, page_count)
        self.setFont("Helvetica", 10)
        self.drawRightString(landscape(A4)[0] - inch, 0.75 * inch, page)

def report_create_pdf(response, title, data):
    """
    View para Gerar Relatório de Exames em PDF com Filtros Aplicados e Personalização
    """

    # Definir a orientação para paisagem e reduzir margens
    doc = SimpleDocTemplate(response, pagesize=landscape(A4), 
                            leftMargin=0.5 * inch, rightMargin=0.5 * inch,
                            topMargin=0.5 * inch, bottomMargin=0.5 * inch)
    elements = []

    # Título
    styles = getSampleStyleSheet()
    title = Paragraph("Exames Realizados no Centro de Provas", styles['Title'])
    elements.append(title)

    # Subtítulo com data de geração
    subtitle = Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles['Heading2'])
    elements.append(subtitle)

    # Estilo para as células da tabela com quebra automática de linha
    cell_style = ParagraphStyle(name='Normal', wordWrap='CJK')

    # Calcular a largura disponível e ajustar as colunas
    page_width = landscape(A4)[0] - 1 * inch  # Subtrair margens (ajuste conforme necessário)
    col_widths = [page_width / len(data[0])] * len(data[0])

    # Criar a tabela com larguras ajustadas para as colunas
    table = Table(data, colWidths=col_widths)

    # Estilo da tabela
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E6B510')),  # Cor de fundo do cabeçalho
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Cor do texto do cabeçalho
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Alinhar texto à esquerda
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),  # Fonte da tabela
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamanho da fonte
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaçamento inferior no cabeçalho
        ('VALIGN', (0, 0), (-1, -1), 'TOP')  # Alinhamento vertical no topo
    ])

    # Adicionar estilo de linhas alternadas
    for i in range(1, len(data)):
        if i % 2 == 0:
            bg_color = colors.HexColor('#e3e3e1')  # Cor de fundo das linhas pares
        else:
            bg_color = colors.white  # Cor de fundo das linhas ímpares
        table_style.add('BACKGROUND', (0, i), (-1, i), bg_color)

    table.setStyle(table_style)

    elements.append(table)

    doc.build(elements, canvasmaker=FooterCanvas)

    return response
