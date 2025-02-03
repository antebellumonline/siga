# reports/utils/excel_utils.py

import openpyxl
from django.http import HttpResponse

def report_create_xlsx(queryset, headers, filename, row_formatter):
    """
    Função para gerar um relatório em Excel a partir de um queryset filtrado.
    
    Args:
        queryset: Queryset filtrado com os dados a serem exportados.
        headers: Lista de cabeçalhos para as colunas do Excel.
        filename: Nome do arquivo Excel a ser gerado.
        row_formatter: Função para formatar cada linha de dados.
    
    Returns:
        HttpResponse: Resposta HTTP com o arquivo Excel para download.
    """
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'

    # Criar o Workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Relatório"

    # Adicionar cabeçalhos
    ws.append(headers)

    # Adicionar dados do queryset
    for obj in queryset:
        row = row_formatter(obj)
        ws.append(row)

    wb.save(response)
    return response
