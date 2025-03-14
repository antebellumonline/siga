# apps/turmas/views.py

"""
Definição das views para o aplicativo 'turmas'.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils.html import format_html

from django.db.models import Q

from .models import Turma, TipoTurma, Curso, Empresa, Local
from .forms import TurmaForm

def turma_home(request):
    """
    View para a Página Inicial das Turmas
    """
    return render(request, 'turmas/turma_home.html')

def turma_new(request):
    """
    View para Adicionar uma Turma
    """
    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('turma_list'))
    else:
        form = TurmaForm()
    return render(request, 'turmas/turma_form.html', {
        'form': form
    })

def turma_list(request):
    """
    View para Listar as Turmas
    """
    # Obtém os filtros
    query = request.GET.get('turma-list-query')
    curso = request.GET.get('curso')
    tipo = request.GET.get('tipo')
    empresa = request.GET.get('empresa')
    local = request.GET.get('local')
    iniciocurso = request.GET.get('inicioCurso')
    enturmacao = request.GET.get('enturmacao')
    plataforma = request.GET.get('plataforma')
    material = request.GET.get('material')
    certificado = request.GET.get('certificado')
    inativo = request.GET.get('inativo')

    # Ordenação
    order_by = request.GET.get('order_by', 'nome')
    descending = request.GET.get('descending', 'True') == 'True'

    # Otimização da Consulta
    turma = Turma.objects.select_related(
        'curso',
        'tipo',
        'empresa',
        'local'
    )

    # Filtragem
    if query:
        turma = turma.filter(
            Q(nome__icontains=query)
        )

    if curso:
        turma = turma.filter(curso__id=curso)

    if tipo:
        turma = turma.filter(tipo__id=tipo)

    if empresa:
        turma = turma.filter(empresa__id=empresa)

    if local:
        turma = turma.filter(local__id=local)

    if iniciocurso:
        turma = turma.filter(inicioCurso=iniciocurso)

    if enturmacao in ['True', 'False']:
        turma = turma.filter(enturmacao=enturmacao == 'True')

    if plataforma in ['True', 'False']:
        turma = turma.filter(plataforma=plataforma == 'True')

    if material in ['True', 'False']:
        turma = turma.filter(material=material == 'True')

    if certificado in ['True', 'False']:
        turma = turma.filter(certificado=certificado == 'True')

    if inativo in ['True', 'False']:
        turma = turma.filter(inativo=inativo == 'True')

    # Aplicação da Ordenação
    if descending:
        order_by = f'-{order_by}'
    turma = turma.order_by(order_by)

    # Registros por Página
    records_per_page = request.GET.get('records_per_page', 20)
    try:
        records_per_page = int(records_per_page)
    except (ValueError, TypeError):
        records_per_page = 20

    # Paginação
    paginator = Paginator(turma, records_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Tratamento de erros para garantir que o objeto de página seja válido
    try:
        page_obj = paginator.get_page(page_number)
    except (ValueError, TypeError):
        page_obj = paginator.get_page(1)

    # Busca e Ordenação das opções de Seleção
    cursos = Curso.objects.order_by('nome')
    tipos = TipoTurma.objects.order_by('nome')
    empresas = Empresa.objects.order_by('razaoSocial')
    locais = Local.objects.order_by('nome')

    # Definição dos Campos de Pesquisa
    search_fields = [
        {
            'id': 'turma-list-query',
            'name': 'turma-list-query',
            'label': 'Busque pelo Nome da Turma: ',
            'placeholder': 'Busque pelo Nome da Turma',
            'type': 'text',
            'value': request.GET.get('q', '')
        },
        {
            'id': 'turma-list-curso',
            'name': 'turma-list-curso',
            'label': 'Curso :',
            'type': 'select',
            'options': [(
                curso.id,
                f"{curso.codigo}: {curso.nome}"
            ) for curso in cursos],
            'selected': request.GET.get('curso', ''),
        },
        {
            'id': 'turma-list-tipo',
            'name': 'turma-list-tipo',
            'label': 'Tipo de Turma :',
            'type': 'select',
            'options': [(
                tipo.id, tipo.nome
            ) for tipo in tipos],
            'selected': request.GET.get('tipo', ''),
        },
        {
            'id': 'turma-list-empresa',
            'name': 'turma-list-empresa',
            'label': 'Empresa contratante da Turma :',
            'type': 'select',
            'options': [(
                empresa.taxId,
                f"{empresa.razaoSocial} - {empresa.taxId}"
            ) for empresa in empresas],
            'selected': request.GET.get('empresa', ''),
        },
        {
            'id': 'turma-list-local',
            'name': 'turma-list-local',
            'label': 'Local :',
            'type': 'select',
            'options': [(
                local.id, local.nome
            ) for local in locais],
            'selected': request.GET.get('local', ''),
        },
    ]
    context = {
        'turma': turma,
        'page_obj': page_obj,
        'search_fields': search_fields,
        'query_params': request.GET.urlencode(),
        'headers': [
            {'field': 'nome', 'label': 'Nome'},
            {'field': 'curso', 'label': 'Curso'},
            {'field': 'tipo', 'label': 'Tipo'},
            {'field': 'empresa', 'label': 'Empresa'},
            {'field': 'local', 'label': 'Local'},
            {'field': 'inicioCurso', 'label': 'Início do Curso'},
            {'field': 'terminoCurso', 'label': 'Término do Curso'},
            {'field': 'datasCurso', 'label': 'Datas do Curso'},
            {'field': 'enturmacao', 'label': 'Enturmação'},
            {'field': 'plataforma', 'label': 'Plataforma'},
            {'field': 'material', 'label': 'Material'},
            {'field': 'certificado', 'label': 'Certificado'},
            {'field': 'observacao', 'label': 'Observação'},
            {'field': 'inativo', 'label': 'Inativo'}
        ],
        'rows': [
            [
                format_html(
                    '<a href="{}" class="turma-mask">{}</a>',
                    reverse("turma_detail", args=[turma.id]),
                    turma.nome
                ),
                turma.curso.nome,
                turma.tipo.nome,
                turma.empresa.razaoSocial,
                turma.local.nome,
                turma.inicioCurso,
                turma.terminoCurso,
                turma.datasCurso,
                "Sim" if turma.enturmacao else "Não",
                "Sim" if turma.plataforma else "Não",
                "Sim" if turma.material else "Não",
                "Sim" if turma.certificado else "Não",
                turma.observacao,
                "Sim" if turma.inativo else "Não",
            ]
            for turma in page_obj
        ]
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'includes/table.html', context)
    else:
        return render(
            request,
            'turmas/turma_list.html',
            context
        )

def turma_detail(request, pk):
    """
    View para Visualizar os detalhes de uma Turma
    """
    # Obtém o objeto pelo ID (pk) ou retorna erro 404 se não encontrado
    turma = get_object_or_404(Turma, pk=pk)

    # Renderização do template
    return render(request, 'turmas/turma_detail.html', {
        'turma': turma
    })

def turma_edit(request, pk):
    """
    View para Editar uma Turma
    """

    # Obtém o objeto pelo ID (pk) ou retorna erro 404 se não encontrado
    turma = get_object_or_404(Turma, pk=pk)

    # Verifica se a requisição é do tipo POST (submissão de formulário)
    if request.method == "POST":
        form = TurmaForm(request.POST, instance=turma)

        # Se o formulário for válido, salva as alterações no objeto
        if form.is_valid():
            form.save()
            return redirect('turma_list')
    else:
        form = TurmaForm(instance=turma)

    # Renderização do template
    return render(request, 'turmas/turma_form.html', {
        'form': form
    })

def turma_delete(request, pk):
    """
    View para Excluir uma Turma
    """
    turma = get_object_or_404(Turma, pk=pk)
    if request.method == "POST":
        turma.delete()
        return redirect('turma_list')
    return render(request, 'turmas/turma_confirm_delete.html', {
        'turma': turma
    })
