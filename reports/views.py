# reports/views.py
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from weasyprint import HTML
from django.template.loader import render_to_string

def gerar_relatorio(request):
    # Lógica para aplicar filtros e gerar relatórios
    filtros = request.GET

    # Adicione a lógica de filtragem aqui
    if 'data_inicio' in filtros:
        relatorios = relatorios.filter(data_criacao__gte=filtros['data_inicio'])
    if 'data_fim' in filtros:
        relatorios = relatorios.filter(data_criacao__lte=filtros['data_fim'])

    if request.GET.get('exportar') == 'excel':
        return exportar_excel(relatorios)
    elif request.GET.get('exportar') == 'pdf':
        return exportar_pdf(relatorios)

    return render(request, 'relatorios/relatorio.html', {'relatorios': relatorios})

def exportar_excel(relatorios):
    df = pd.DataFrame(list(relatorios.values()))
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=relatorio.xlsx'
    df.to_excel(response, index=False)
    return response

def exportar_pdf(relatorios):
    html_string = render_to_string('relatorios/relatorio_pdf.html', {'relatorios': relatorios})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=relatorio.pdf'
    HTML(string=html_string).write_pdf(response)
    return response
