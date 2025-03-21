# apps/centroProva/views.py

"""
Definição das views para o aplicativo 'centroProva'.
"""

from datetime import datetime, timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Q

from django.http import HttpResponse
from django.utils import timezone
from django.utils.safestring import mark_safe
from reports.utils.pdf_utils import report_create_pdf
from reports.utils.excel_utils import report_create_xlsx

from .models import CentroProva, CentroProvaExame, Aluno, Certificacao
from .forms import CentroProvaForm, CentroProvaExameForm

def centroprova_home(request):
    """
    View para a Página Inicial do Centro de Provas
    """
    return render(request, 'centroProva/centroProva_home.html')

def centroprova_new(request):
    """
    View para Adicionar um Centro de Provas
    """
    if request.method == 'POST':
        form = CentroProvaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('centroprova_list'))
        else:
            print(form.errors)
    else:
        form = CentroProvaForm()

    # Definição das Seções e Botões
    sections = [
        {
            'title': 'Dados do Centro de Provas',
            'fields': [
                form['nome'],
            ]
        },
    ]

    buttons = [
        {
            'class': 'btn-return',
            'url': reverse('centroprova_list'),
            'title': 'Retornar',
            'text': 'Retornar',
        },
    ]

    # Renderização do template
    return render(request, 'centroProva/centroProva_form.html', {
        'form': form,
        'sections': sections,
        'buttons': buttons,
    })

def centroprova_list(request):
    """
    View para Listar os Centros de Provas    
    """
    # Obtém os filtros
    query = request.GET.get('centroProva-list-query')
    inativo = request.GET.get('centroProva-list-inativo')

    # Ordenação
    order_by = request.GET.get('order_by', 'nome')
    descending = request.GET.get('descending', 'False') == 'True'

    # Otimização da Consulta
    centroprova = CentroProva.objects.all()

    # Filtragem
    if query:
        centroprova = centroprova.filter(
            Q(id__icontains=query) |
            Q(nome__icontains=query)
        )

    if inativo in ['True', 'False']:
        centroprova = centroprova.filter(inativo=inativo == 'True')

    # Aplicação da Ordenação
    if descending:
        order_by = f'-{order_by}'
    centroprova = centroprova.order_by(order_by)

    # Registros por Página
    records_per_page = request.GET.get('records_per_page', 20)
    try:
        records_per_page = int(records_per_page)
    except (ValueError, TypeError):
        records_per_page = 10

    # Paginação
    paginator = Paginator(centroprova, records_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Tratamento de erros para garantir que o objeto de página seja válido
    try:
        page_obj = paginator.get_page(page_number)
    except (ValueError, TypeError):
        page_obj = paginator.get_page(1)

    # Definição dos Campos de Pesquisa
    search_fields = [
        {
            'id': 'centroProva-list-query',
            'name': 'centroProva-list-query',
            'label': 'Busque pelo Nome ou ID do Centro de Provas:',
            'placeholder': 'Busque pelo Nome ou ID do Centro de Provas',
            'type': 'text',
            'value': request.GET.get('q', ''),
        },
        {
            'id': 'centroProva-list-inativo',
            'name': 'centroProva-list-inativo',
            'label': 'Centro de Provas Inativo?',
            'type': 'select',
            'options': [('True', 'Sim'), ('False', 'Não')],
            'selected': request.GET.get('inativo', ''),
        },
    ]

    context = {
        'centroprova': centroprova,
        'page_obj': page_obj,
        'search_fields': search_fields,
        'query_params': request.GET.urlencode(),
        'headers': [
            {'field': 'id', 'label': 'ID'},
            {'field': 'nome', 'label': 'Nome'},
            {'field': 'inativo', 'label': 'Inativo'}
        ],
        'rows': [
            [
                centroprova.id,
                mark_safe(
                    f'<a href="{reverse(
                        "centroprova_detail",
                        args=[centroprova.id]
                    )}">{centroprova.nome}</a>'
                ),
                "Sim" if centroprova.inativo else "Não",
            ]
            for centroprova in page_obj
        ]
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'includes/table.html', context)
    else:
        return render(
            request,
            'centroProva/centroProva_list.html',
            context
        )

def centroprova_detail(request, pk):
    """
    View para Visualizar os detalhes de um Centro de Provas   
    """
    # Obtenção dos filtros
    centroprova = get_object_or_404(CentroProva, pk=pk)

    # Preparação dos Dados para o template reutilizável
    tabs = [
        {
            'id': 'centroProva-detail-dados',
            'class': 'btn-detail',
            'label': 'Detalhes'
        },
    ]

    sections = [
        {
            'id': 'centroProva-detail-dados',
            'title': 'Detalhes do Centro de Provas',
            'active': True,
            'fields': [
                {
                    'label': 'Status do Centro de Provas',
                    'value': 'Inativo' if centroprova.inativo else 'Ativo'
                },
                {'label': 'Nome', 'value': centroprova.nome},
            ]
        },
    ]

    buttons = [
        {
            'class': 'btn-edit',
            'url': reverse('centroprova_edit', args=[centroprova.pk]),
            'title': 'Editar Centro de Provas',
            'aria-label': 'Editar Centro de Provas',
        },
        {
            'class': 'btn-delete',
            'url': '#',
            'data': {'model': 'CentroProva','pk': centroprova.pk},
            'title': 'Excluir Centro de Provas',
        'aria-label': 'Excluir Centro de Provas',
        },
        {
            'class': 'btn-return',
            'url': reverse('centroprova_list'),
            'title': 'Voltar para a lista de Centros de Provas',
            'aria-label': 'Voltar para a lista de Centros de Provas',
        },
    ]

    # Renderização do template
    return render(request, 'centroProva/centroProva_detail.html', {
        'centroprova': centroprova,
        'tabs': tabs,
        'sections': sections,
        'buttons': buttons,
    })

def centroprova_edit(request, pk):
    """
    View para Editar um Centro de Provas
    """
    # Obtém o objeto pelo ID (pk) ou retorna erro 404 se não encontrado
    centroprova = get_object_or_404(CentroProva, pk=pk)

    # Verifica se a requisição é do tipo POST (submissão de formulário)
    if request.method == "POST":
        form = CentroProvaForm(request.POST, instance=centroprova)

        # Se o formulário for válido, salva as alterações no objeto
        if form.is_valid():
            form.save()
            return redirect('centroProva_list')
    else:
        form = CentroProvaForm(instance=centroprova)

    # Definição das Seções e Botões
    sections = [
        {
            'title': 'Dados do Centro de Provas',
            'fields': [
                form['inativo'],
                form['nome'],
            ]
        },
    ]

    buttons = [
        {
            'class': 'btn-return',
            'url': reverse('centroprova_list'),
            'title': 'Retornar',
            'text': 'Retornar',
        },
    ]

    # Renderização do template
    return render(request, 'centroProva/centroProva_form.html', {
        'form': form,
        'sections': sections,
        'buttons': buttons,
    })

def centroprova_delete(request, pk):
    """
    View para Excluir um Centro de Provas
    """
    centroprova = get_object_or_404(CentroProva, pk=pk)
    if request.method == "POST":
        centroprova.delete()
        return redirect('centroProva_list')
    return render(request, 'centroProva/centroProva_confirmDelete.html', {
        'centroprova': centroprova
    })

# ----- XXXXX ----- XXXXX -----

def exame_new(request):
    """
    View para Adicionar um Exame Realizado no Centro de Provas
    """

    if request.method == 'POST':
        form = CentroProvaExameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exame_list')
        else:
            print(form.errors)
    else:
        form = CentroProvaExameForm()

    # Definição das Seções e Botões
    sections = [
        {
            'title': 'Dados do Exame Realizado no Centro de Provas',
            'fields': [
                form['data'],
                form['centroProva'],
                form['certificacao'],
                form['aluno'],
                form['presenca'],
                form['cancelado'],
                form['observacao'],
            ]
        },
    ]

    buttons = [
        {
            'class': 'btn-return',
            'url': reverse('exame_list'),
            'title': 'Retornar',
            'text': 'Retornar',
        },
    ]

    # Renderização do template
    return render(request, 'centroProva/centroProva-exame_form.html', {
        'form': form,
        'sections': sections,
        'buttons': buttons,
    })

def exame_list(request):
    """
    View para Listar os Exames Realizados no Centro de Provas
    """
    # Obtém os filtros
    aluno = request.GET.get('exame-list-aluno')
    data_range = request.GET.get('exame-list-daterange')
    presenca = request.GET.get('exame-list-presenca')
    cancelado = request.GET.get('exame-list-cancelado')
    centroprova = request.GET.get('exame-list-centroProva')
    certificacao = request.GET.get('exame-list-certificacao')

    # Ordenação
    order_by = request.GET.get('order_by', 'data')
    descending = request.GET.get('descending', 'True') == 'True'

    # Otimização de Consulta
    centroprova_exame = CentroProvaExame.objects.select_related(
        'aluno',
        'centroProva',
        'certificacao'
    )

    # Filtra por Aluno
    if aluno:
        centroprova_exame = centroprova_exame.filter(aluno__uid=aluno)

    # Filtra por Período
    if data_range:
        try:
            data_inicio, data_fim = data_range.split(' - ')
            data_inicio = datetime.strptime(data_inicio.strip(), '%d/%m/%Y').date()
            data_fim = datetime.strptime(data_fim.strip(), '%d/%m/%Y').date()
            data_fim += timedelta(days=1)
            centroprova_exame = centroprova_exame.filter(data__range=[data_inicio, data_fim])
        except (ValueError, TypeError):
            pass

    # Filtra por Presença
    if presenca in ['True', 'False']:
        centroprova_exame = centroprova_exame.filter(presenca=presenca == 'True')

    # Filtra por Cancelado
    if cancelado in ['True', 'False']:
        centroprova_exame = centroprova_exame.filter(cancelado=cancelado == 'True')

    # Filtra por Centro de Prova
    if centroprova:
        centroprova_exame = centroprova_exame.filter(centroProva__id=centroprova)

    # Filtra por Certificação
    if certificacao:
        centroprova_exame = centroprova_exame.filter(certificacao__id=certificacao)

    # Aplicar ordenação
    if descending:
        order_by = f'-{order_by}'
    centroprova_exame = centroprova_exame.order_by(order_by)

    # Quantidade de registros por página (com valor padrão de 20)
    records_per_page = request.GET.get('records_per_page', 20)
    try:
        records_per_page = int(records_per_page)
    except (ValueError, TypeError):
        records_per_page = 20

    # Criação do paginator com o queryset e o número de registros por página
    paginator = Paginator(centroprova_exame, records_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Tratamento de erros para garantir que o objeto de página seja válido
    try:
        page_obj = paginator.get_page(page_number)
    except (ValueError, TypeError):
        page_obj = paginator.get_page(1)

    # Buscar e ordenar opções de seleção
    alunos = Aluno.objects.order_by('nome')
    centrosprova = CentroProva.objects.order_by('nome')
    certificacoes = Certificacao.objects.order_by('descricao')

    # Definindo os campos de pesquisa
    search_fields = [
        {
            'type': 'daterange',
            'id': 'exame-list-daterange',
            'name': 'exame-list-daterange',
            'class': 'apps-list-search-form daterange',
            'label': 'Período de realização',
            'value': request.GET.get('daterange', ''),
        },
        {
            'id': 'exame-list-aluno',
            'name': 'exame-list-aluno',
            'label': 'Aluno',
            'type': 'select',
            'options': [(aluno.uid, f"{aluno.uid} - {aluno.nome}") for aluno in alunos],
            'selected': request.GET.get('aluno', ''),
        },
        {
            'id': 'exame-list-centroProva',
            'name': 'exame-list-centroProva',
            'label': 'Centro de Provas',
            'type': 'select',
            'options': [
                (centroprova.id, centroprova.nome) for centroprova in centrosprova
            ],
            'selected': request.GET.get('centroProva', ''),
        },
        {
            'id': 'exame-list-certificacao',
            'name': 'exame-list-certificacao',
            'label': 'Certificação',
            'type': 'select',
            'options': [
                (
                    certificacao.id,
                    f"{certificacao.descricao} ({certificacao.siglaExame})"
                ) for certificacao in certificacoes
            ],
            'selected': request.GET.get('certificacao', ''),
        },
        {
            'id': 'exame-list-presenca',
            'name': 'exame-list-presenca',
            'label': 'Aluno Presente?',
            'type': 'select',
            'options': [('True', 'Sim'), ('False', 'Não')],
            'selected': request.GET.get('presenca', ''),
        },
        {
            'id': 'exame-list-cancelado',
            'name': 'exame-list-cancelado',
            'label': 'Exame Cancelado?',
            'type': 'select',
            'options': [('True', 'Sim'), ('False', 'Não')],
            'selected': request.GET.get('cancelado', ''),
        },
    ]

    context = {
        'centroprova_exame': centroprova_exame,
        'page_obj': page_obj,
        'search_fields': search_fields,
        'query_params': request.GET.urlencode(),
        'headers': [
            {'field': 'data', 'label': 'Data e Hora'},
            {'field': 'aluno__nome', 'label': 'Aluno'},
            {'field': 'centroProva__nome', 'label': 'Centro de Provas'},
            {'field': 'certificacao__descricao', 'label': 'Certificação'},
            {'field': 'presenca', 'label': 'Presença'},
            {'field': 'cancelado', 'label': 'Cancelado'},
            {'field': 'observacao', 'label': 'Observações'},
        ],
        'rows': [
            [
                timezone.localtime(exame.data).strftime("%d/%m/%Y %H:%M"),
                mark_safe(
                    f'<a href="{reverse(
                        "exame_detail",
                        args=[exame.id]
                    )}">{exame.aluno.nome}</a>'
                ),
                exame.centroProva.nome,
                f"{exame.certificacao.descricao} ({exame.certificacao.siglaExame})",
                "Sim" if exame.presenca else "Não",
                "Sim" if exame.cancelado else "Não",
                exame.observacao,
            ]
            for exame in page_obj
        ]
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'includes/table.html', context)
    else:
        return render(
            request,
            'centroProva/centroProva-exame_list.html',
            context
        )

def exame_detail(request, pk):
    """
    View para Visualizar os Detalhes de um Exame Realizado no Centro de Provas
    """
    # Obtém o objeto pelo ID (pk) ou retorna erro 404 se não encontrado
    centroprova_exame = get_object_or_404(CentroProvaExame, pk=pk)

    # Preparação dos Dados para o template reutilizável
    tabs = [
        {
            'id': 'exame-detail-dados',
            'class': 'btn-detail',
            'label': 'Detalhes'
        },
    ]

    sections = [
        {
            'id': 'exame-detail-dados',
            'title': 'Detalhes do Exame Realizado no Centro de Provas',
            'active': True,
            'fields': [
                {'label': 'ID', 'value': centroprova_exame.id,},
                {'label': 'Data do Exame', 'value': centroprova_exame.data},
                {'label': 'Centro de Provas', 'value': centroprova_exame.centroProva.nome},
                {
                    'label': 'Certificação',
                    'value': (
                        f"{centroprova_exame.certificacao.descricao} "
                        f"({centroprova_exame.certificacao.siglaExame})"
                        if centroprova_exame.certificacao.siglaExame
                        else centroprova_exame.certificacao.descricao
                    )
                },
                {
                    'label': 'Aluno',
                    'value': (
                        f"{centroprova_exame.aluno.uid} - "
                        f"{centroprova_exame.aluno.nome}"
                    )
                },
                {
                    'label': 'O Aluno estava Presente?',
                    'value': 'Sim' if centroprova_exame.presenca else 'Não'
                },
                {
                    'label': 'O Exame foi Cancelado?',
                    'value': 'Sim' if centroprova_exame.cancelado else 'Não'
                },
                {'label': 'Observações do Exame', 'value': centroprova_exame.observacao},
            ]
        },
    ]

    buttons = [
        {
            'class': 'btn-edit',
            'url': reverse('exame_edit', args=[centroprova_exame.pk]),
            'title': 'Editar',
            'aria-label': 'Editar Exame Realizado no Centro de Provas',
        },
        {
            'class': 'btn-delete',
            'url': '#',
            'data': {'model': 'CentroProvaExame','pk': centroprova_exame.pk},
            'title': 'Excluir',
        'aria-label': 'Excluir Exame Realizado no Centro de Provas',
        },
        {
            'class': 'btn-return',
            'url': reverse('exame_list'),
            'title': 'Voltar para a lista de Centros de Provas',
            'aria-label': 'Voltar para a lista de Centros de Provas',
        },
    ]

    # Renderização do template
    return render(request, 'centroProva/centroProva-exame_detail.html', {
        'centroprova_exame': centroprova_exame,
        'tabs': tabs,
        'sections': sections,
        'buttons': buttons,
    })

def exame_edit(request, pk):
    """
    View para Editar um Exame Realizado no Centro de Provas
    """
    # Obtém os filtros
    exame = get_object_or_404(CentroProvaExame, pk=pk)

    # Verifica se a requisição é do tipo POST (submissão de formulário)
    if request.method == "POST":
        form = CentroProvaExameForm(request.POST, instance=exame)

        # Se o formulário for válido, salva as alterações no objeto
        if form.is_valid():
            form.save()
            return redirect('exame_list')
    else:
        form = CentroProvaExameForm(instance=exame)

    # Definição das Seções e Botões
    sections = [
        {
            'title': 'Dados do Exame Realizado no Centro de Provas',
            'fields': [
                form['data'],
                form['centroProva'],
                form['certificacao'],
                form['aluno'],
                form['presenca'],
                form['cancelado'],
                form['observacao'],
            ]
        },
    ]
    buttons = [
        {
            'class': 'btn-return',
            'url': reverse('exame_list'),
            'title': 'Retornar',
            'text': 'Retornar',
        },
    ]

    # Renderização do template
    return render(request, 'centroProva/centroProva-exame_form.html', {
        'form': form,
        'sections': sections,
        'buttons': buttons,
    })

def exame_delete(request, pk):
    """
    View para Excluir um Centro de Provas
    """
    exame = get_object_or_404(CentroProvaExame, pk=pk)

    if request.method == "POST":
        exame.delete()
        return redirect('exame_list')

    return render(request, 'centroProva/centroProva-exame_confirm_delete.html', {
        'exame': exame
    })

def exame_get_filter(request):
    """
    Função auxiliar para obter exames filtrados com base nos parâmetros da requisição.
    """
    aluno = request.GET.get('aluno')
    data_range = request.GET.get('daterange')
    presenca = request.GET.get('presenca')
    cancelado = request.GET.get('cancelado')
    centroprova = request.GET.get('centroProva')
    certificacao = request.GET.get('certificacao')

    centroprova_exame = CentroProvaExame.objects.select_related(
        'aluno', 'centroProva', 'certificacao'
    )

    if aluno:
        centroprova_exame = centroprova_exame.filter(aluno__uid=aluno)
    if data_range:
        try:
            data_inicio, data_fim = data_range.split(' - ')
            data_inicio = datetime.strptime(data_inicio.strip(), '%d/%m/%Y').date()
            data_fim = datetime.strptime(data_fim.strip(), '%d/%m/%Y').date()
            centroprova_exame = centroprova_exame.filter(data__range=[data_inicio, data_fim])
        except (ValueError, TypeError):
            pass
    if presenca in ['True', 'False']:
        centroprova_exame = centroprova_exame.filter(presenca=presenca == 'True')
    if cancelado in ['True', 'False']:
        centroprova_exame = centroprova_exame.filter(cancelado=cancelado == 'True')
    if centroprova:
        centroprova_exame = centroprova_exame.filter(centroProva__id=centroprova)
    if certificacao:
        centroprova_exame = centroprova_exame.filter(certificacao__id=certificacao)

    # Adiciona a ordenação pela data do exame em ordem crescente
    centroprova_exame = centroprova_exame.order_by('data')

    return centroprova_exame

def exame_report_pdf(request):
    """
    View para Gerar Relatório de Exames em PDF com Filtros Aplicados e Personalização
    """
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        'attachment; filename="Exames Realizados no Centro de Provas.pdf"'
    )

    # Dados dos exames
    exames = exame_get_filter(request)
    data = [[
        'Data do Exame',
        'Centro de Provas',
        'Certificação',
        'Aluno',
        'Presença',
        'Cancelado',
        'Observação'
    ]]

    for exame in exames:
        certificacao_text = (
            f"{exame.certificacao.descricao} ({exame.certificacao.siglaExame})"
            if exame.certificacao.siglaExame
            else exame.certificacao.descricao
        )
        aluno_text = f"{exame.aluno.uid} - {exame.aluno.nome}"
        presenca_text = "Presente" if exame.presenca else "Ausente"

        data.append([
            exame.data.strftime('%d/%m/%Y %H:%M:%S'),
            str(exame.centroProva),
            certificacao_text,
            aluno_text,
            presenca_text,
            'Sim' if exame.cancelado else 'Não',
            exame.observacao or ''
        ])

    return report_create_pdf(
        response,
        "Exames Realizados no Centro de Provas",
        data,
        orientation='portrait',
        group_by=1  # Índice da coluna "Centro de Provas"
    )

def exame_report_xlsx(request):
    """
    View para Gerar Relatório de Exames em Excel com Filtros Aplicados
    """
    # Dados dos exames
    exames = exame_get_filter(request)

    # Cabeçalhos do relatório
    headers = [
        'Data do Exame',
        'Centro de Provas',
        'Certificação',
        'Aluno',
        'Presença',
        'Cancelado',
        'Observação'
    ]

    # Nome do arquivo
    filename = "Exames Realizados no Centro de Provas"

    # Função para formatar cada linha de dados
    def format_row(exame):
        certificacao_text = (
            f"{exame.certificacao.descricao} ({exame.certificacao.siglaExame})"
            if exame.certificacao.siglaExame
            else exame.certificacao.descricao
        )
        aluno_text = f"{exame.aluno.uid} - {exame.aluno.nome}"
        presenca_text = "Presente" if exame.presenca else "Ausente"

        return [
            exame.data.strftime('%d/%m/%Y %H:%M:%S'),
            str(exame.centroProva),
            certificacao_text,
            aluno_text,
            presenca_text,
            'Sim' if exame.cancelado else 'Não',
            exame.observacao or ''
        ]

    # Gerar e retornar o relatório em Excel
    return report_create_xlsx(exames, headers, filename, format_row)
