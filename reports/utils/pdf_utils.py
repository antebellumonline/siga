# reports/utils/pdf_utils.py

"""
Módulo para gerar relatórios em PDF para os apps do projeto.
"""

from datetime import datetime
from babel.dates import format_datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import ParagraphStyle

def draw_header(canvas, doc, title):
    """
    Desenha o cabeçalho do relatório com fundo colorido, espaço para logo e título ajustável.
    """
    # O argumento 'doc' é necessário para compatibilidade com outras partes do código
    _ = doc

    canvas.saveState()

    page_width, page_height = landscape(A4)
    header_height = 1.2 * inch
    logo_width = page_width * 0.25  # 25% da largura
    text_width = page_width * 0.75  # 75% da largura
    padding = 0.2 * inch  # Espaçamento interno

    # Fundo do cabeçalho
    canvas.setFillColor(colors.HexColor("#1a4f45"))
    canvas.rect(0, page_height - header_height, page_width, header_height, fill=True, stroke=False)

    # Caminho para a imagem
    logo_path = "static/images/logo-antebellum-horizontal-2linhas-negativo-verdeEscuro.png"

    # Carregar a imagem usando ImageReader
    logo_image = ImageReader(logo_path)
    original_width, original_height = logo_image.getSize()

    # Calcular a nova largura e altura mantendo a proporção
    aspect_ratio = original_width / original_height
    new_width = logo_width - padding
    new_height = new_width / aspect_ratio

    # Verificar se a nova altura excede o limite permitido
    if new_height > (header_height - padding):
        new_height = header_height - padding
        new_width = new_height * aspect_ratio

    # Inserir a imagem no canvas
    logo = Image(logo_path, width=new_width, height=new_height)
    logo.drawOn(canvas, padding, page_height - header_height + padding)

    # Ajuste automático do tamanho do título
    max_font_size = 22
    min_font_size = 12
    font_name = "Helvetica-Bold"
    text_x = logo_width + padding
    text_y = page_height - (header_height / 2)
    text_max_width = text_width - 2 * padding

    font_size = max_font_size
    while (canvas.stringWidth(title, font_name, font_size) > text_max_width and
           font_size > min_font_size):
        font_size -= 1

    canvas.setFillColor(colors.white)
    canvas.setFont(font_name, font_size)
    canvas.drawCentredString(text_x + (text_width / 2), text_y, title)

    canvas.restoreState()

def draw_footer(c, page_number):
    """Desenha o rodapé em todas as páginas."""
    now = datetime.now()
    generated_text = (
        f"Gerado em: {format_datetime(now, 'd \'de\' MMMM \'de\' y \'às\' HH:mm:ss',
        locale='pt_BR')}"
    )
    page_text = f"{page_number}"

    # Cor de fundo do rodapé
    c.setFillColor(colors.HexColor("#1a4f45"))
    c.rect(0, 0, landscape(A4)[0], 0.5 * inch, fill=True, stroke=False)

    # Cor do texto do rodapé
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(inch, 0.25 * inch, generated_text)

    # Desenhar círculo com número da página
    c.setFillColor(colors.HexColor("#E6B510"))
    c.circle(landscape(A4)[0] - inch, 0.25 * inch, 0.2 * inch, fill=True, stroke=False)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(landscape(A4)[0] - inch, 0.25 * inch - 0.05 * inch, page_text)

def on_page(c, doc, title):
    """Desenha o cabeçalho e o rodapé na página."""
    draw_header(c, doc, title)
    draw_footer(c, doc.page)

def report_create_pdf(response, title, data):
    """
    Gera o relatório em PDF com cabeçalho padronizado e tabela formatada.
    """
    doc = SimpleDocTemplate(response,
                            pagesize=landscape(A4),
                            leftMargin=0.5 * inch,
                            rightMargin=0.5 * inch,
                            topMargin=1.2 * inch,
                            bottomMargin=0.5 * inch
                            )
    elements = []

    # Estilo das células da tabela
    cell_style = ParagraphStyle(name='Normal', wordWrap='CJK')
    header_style = ParagraphStyle(name='Header', fontName='Helvetica-Bold', wordWrap='CJK')
    data = [
        [Paragraph(str(cell), header_style if i == 0 else cell_style) for cell in row]
        for i, row in enumerate(data)
    ]

    # Criar tabela
    col_widths = [landscape(A4)[0] / len(data[0])] * len(data[0])
    table = Table(data, colWidths=col_widths, repeatRows=1)

    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E6B510')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ])

    # Adicionar cores alternadas nas linhas
    for i in range(1, len(data)):
        bg_color = colors.HexColor('#e3e3e1') if i % 2 == 0 else colors.white
        table_style.add('BACKGROUND', (0, i), (-1, i), bg_color)

    table.setStyle(table_style)
    elements.append(table)

    # Adicionando cabeçalho e rodapé em cada página
    doc.build(elements, onFirstPage=lambda c, d: on_page(c, d, title),
                     onLaterPages=lambda c, d: on_page(c, d, title))

    return response
