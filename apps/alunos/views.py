# alunos/views.py

"""
Definição das views para o aplicativo 'alunos'.

As views utilizam Django para gerenciar as requisições HTTP 
e interagir com os modelos de dados.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q

from apps.cidades.models import Cidade
from .models import Aluno, AlunoContato
from .forms import AlunoForm, AlunoContatoFormSet

def aluno_home(request):
    """
    View para a Página Inicial de Alunos
    """
    return render(request, 'alunos/aluno_home.html')

def aluno_new(request):
    """
    View para Adicionar um Aluno
    """
    cidades = Cidade.objects.select_related('estado').order_by('nome')

    if request.method == "POST":
        form = AlunoForm(request.POST)
        formset = AlunoContatoFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            aluno = form.save()
            formset.instance = aluno
            formset.save()
            return redirect('aluno_list')
    else:
        form = AlunoForm()
        formset = AlunoContatoFormSet()

    return render(request, 'alunos/aluno_form.html', {
        'form': form,
        'formset': formset,
        'cidades': cidades
    })

def aluno_list(request):
    """
    View para Listar os Alunos
    """
    # Obtém os filtros
    query = request.GET.get('q')
    inativo = request.GET.get('inativo')
    cidade = request.GET.get('cidade')

    # Ordenação
    order_by = request.GET.get('order_by', 'nome')
    descending = request.GET.get('descending', 'False') == 'True'

    # Otimiza a consulta usando select_related para carregar cidade junto com aluno
    alunos = Aluno.objects.prefetch_related('contatos', 'cidade', 'cidade__estado').all()

    # Aplicar os filtros e pesquisa
    if query:
        alunos = alunos.filter(
            Q(uid__icontains=query) |
            Q(nome__icontains=query) |
            Q(contatos__contato__icontains=query) |
            Q(contatos__detalhe__icontains=query)
        ).distinct()

    # Filtra por Status
    if inativo is not None and inativo != "":  # Verifica se o filtro foi aplicado
        if inativo == 'True':
            alunos = alunos.filter(inativo=True)
        elif inativo == 'False':
            alunos = alunos.filter(inativo=False)

    # Filtra por Cidade
    if cidade:
        alunos = alunos.filter(cidade__nome=cidade)  # Filtra por Cidade

    # Aplicar ordenação
    if descending:
        order_by = f'-{order_by}'
    alunos = alunos.order_by(order_by)

    # Quantidade de registros por página (com valor padrão de 20)
    records_per_page = request.GET.get('records_per_page', 20)
    try:
        records_per_page = int(records_per_page)
    except (ValueError, TypeError):
        records_per_page = 20

    # Criação do paginator com o queryset e o número de registros por página
    paginator = Paginator(alunos, records_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Tratamento de erros para garantir que o objeto de página seja válido
    try:
        page_obj = paginator.get_page(page_number)
    except (ValueError, TypeError):
        page_obj = paginator.get_page(1)

    # Buscar e ordenar opções de seleção
    cidades = Cidade.objects.select_related('estado').all().order_by('nome')

    # Renderização do template
    return render(request, 'alunos/aluno_list.html', {
        'alunos': alunos,
        'page_obj': page_obj,
        'cidades': cidades,
        'query_params': request.GET,
    })

def aluno_detail(request, pk):
    """
    View para Visualizar os detalhes de um Aluno
    """
    # Obtém os filtros
    aluno = get_object_or_404(Aluno, pk=pk)
    contatos = AlunoContato.objects.filter(aluno=aluno).order_by('tipoContato__descricao')

    # Renderização do template
    return render(request, 'alunos/aluno_detail.html', {
        'aluno': aluno,
        'contatos': contatos
    })

def aluno_edit(request, pk):
    """
    View para Editar um Aluno
    """
    aluno = get_object_or_404(Aluno, pk=pk)
    cidades = Cidade.objects.select_related('estado').order_by('nome')

    if request.method == "POST":
        form = AlunoForm(request.POST, instance=aluno)
        formset = AlunoContatoFormSet(request.POST, instance=aluno)

        print(request.POST)  # Adicionado para depuração

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('aluno_list')
        else:
            print(form.errors)
            for contato_form in formset:
                print(contato_form.errors)
    else:
        form = AlunoForm(instance=aluno)
        formset = AlunoContatoFormSet(instance=aluno)

    return render(request, 'alunos/aluno_form.html', {
        'form': form,
        'formset': formset,
        'cidades': cidades
    })

def aluno_delete(request, pk):
    """
    View para Excluir um Aluno
    """
    aluno = get_object_or_404(Aluno, pk=pk)
    if request.method == "POST":
        aluno.delete()
        return redirect('aluno_list')
    return render(request, 'alunos/aluno_confirm_delete.html', {'aluno': aluno})
