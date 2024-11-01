# apps/centroProva/views.py

"""
Definição das views para o aplicativo 'centroProva'.

As views utilizam Django para gerenciar as requisições HTTP 
e interagir com os modelos de dados.
"""

from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Q

from .models import CentroProva, CentroProvaExame, Aluno, Certificacao
from .forms import CentroProvaForm, CentroProvaExameForm

@login_required
def home(request):
    """
    View para a Página Inicial do Projeto
    """
    return render(request, 'home.html')

def login_view(request):
    """
    View para a Página de Login
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {
        'form': form
    })

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
            return redirect(reverse('centroProva_list'))
    else:
        form = CentroProvaForm()
    return render(request, 'centroProva/centroProva_form.html', {
        'form': form
    })

def centroprova_list(request):
    """
    View para Listar os Centros de Provas    
    """
    # Obtém os filtros
    query = request.GET.get('q')
    inativo = request.GET.get('inativo')

    # Ordenação
    order_by = request.GET.get('order_by', 'nome')
    descending = request.GET.get('descending', 'False') == 'True'

    # Inicializa a variável centroProva
    centroprova = CentroProva.objects.all()

    # Aplicar os filtros e pesquisa
    if query:
        centroprova = centroprova.filter(
            Q(id__icontains=query) |
            Q(nome__icontains=query)
        )

    # Filtra por Status
    if inativo is not None and inativo != "":
        if inativo == 'True':
            centroprova = centroprova.filter(inativo=True)
        elif inativo == 'False':
            centroprova = centroprova.filter(inativo=False)

    # Aplicar ordenação
    if descending:
        order_by = f'-{order_by}'
    centroprova = centroprova.order_by(order_by)

    # Quantidade de registros por página (com valor padrão de 20)
    records_per_page = request.GET.get('records_per_page', 20)
    try:
        records_per_page = int(records_per_page)
    except (ValueError, TypeError):
        records_per_page = 10

    # Criação do paginator com o queryset e o número de registros por página
    paginator = Paginator(centroprova, records_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Tratamento de erros para garantir que o objeto de página seja válido
    try:
        page_obj = paginator.get_page(page_number)
    except (ValueError, TypeError):
        page_obj = paginator.get_page(1)

    # Renderização do template
    return render(request, 'centroProva/centroProva_list.html', {
        'centroprova': centroprova,
        'page_obj': page_obj,
        'query_params': request.GET,
        })

def centroprova_detail(request, pk):
    """
    View para Visualizar os detalhes de um Centro de Provas   
    """
    # Obtém o objeto pelo ID (pk) ou retorna erro 404 se não encontrado
    centroprova = get_object_or_404(CentroProva, pk=pk)

    # Renderização do template
    return render(request, 'centroProva/centroProva_detail.html', {
        'centroprova': centroprova
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

    # Renderização do template
    return render(request, 'centroProva/centroProva_form.html', {
        'form': form
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
    alunos = Aluno.objects.order_by('nome')
    centrosprovas = CentroProva.objects.order_by('nome')
    certificacoes = Certificacao.objects.order_by('descricao')

    if request.method == 'POST':
        form = CentroProvaExameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exame_list')
        else:
            print(form.errors)
    else:
        form = CentroProvaExameForm()

    return render(request, 'centroProva/centroProva-exame_form.html', {
        'form': form, 
        'alunos': alunos,
        'centrosprovas': centrosprovas,
        'certificacoes': certificacoes
    })

def exame_list(request):
    """
    View para Listar os Exames Realizados no Centro de Provas
    """
    # Obtém os filtros
    query = request.GET.get('q')
    data_range = request.GET.get('daterange')
    presenca = request.GET.get('presenca')
    cancelado = request.GET.get('cancelado')
    centroprova = request.GET.get('centroProva')
    certificacao = request.GET.get('certificacao')

    # Ordenação
    order_by = request.GET.get('order_by', 'data')
    descending = request.GET.get('descending', 'False') == 'True'

    # Otimização de Consulta
    centroprova_exame = CentroProvaExame.objects.select_related(
        'aluno',
        'centroProva',
        'certificacao'
    )

    # Aplicar os filtros e pesquisa
    if query:
        centroprova_exame = centroprova_exame.filter(
            Q(aluno__uid__icontains=query) |
            Q(aluno__nome__icontains=query)
        )

    # Filtra por Período
    if data_range:
        try:
            data_inicio, data_fim = data_range.split(' - ')
            # Converte o formato de DD/MM/YYYY para YYYY-MM-DD
            data_inicio = datetime.strptime(data_inicio.strip(), '%d/%m/%Y').date()
            data_fim = datetime.strptime(data_fim.strip(), '%d/%m/%Y').date()
            centroprova_exame = centroprova_exame.filter(data__range=[data_inicio, data_fim])
        except (ValueError, TypeError):
            pass  # Ignorar filtro em caso de erro

    # Filtra por Presença
    if presenca in ['True', 'False']:
        centroprova_exame = centroprova_exame.filter(presenca=presenca == 'True')

    # Filtra por Cancelado
    if cancelado in ['True', 'False']:
        centroprova_exame = centroprova_exame.filter(cancelado=cancelado == 'True')

    # Filtra por Centro de Prova
    if centroprova:
        centroprova_exame = centroprova_exame.filter(centroprova__id=centroprova)

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

    return render(request, 'centroProva/centroProva-exame_list.html', {
        'centroprova_exame': centroprova_exame,
        'page_obj': page_obj,
        'aluno': alunos,
        'centrosprova': centrosprova,
        'certificacao': certificacoes,
        'query_params': request.GET.urlencode(),
    })

def exame_detail(request, pk):
    """
    View para Visualizar os Detalhes de um Exame Realizado no Centro de Provas
    """
    # Obtém o objeto pelo ID (pk) ou retorna erro 404 se não encontrado
    centroprova_exame = get_object_or_404(CentroProvaExame, pk=pk)

    # Renderização do template
    return render(request, 'centroProva/centroProva-exame_detail.html', {
        'centroprova_exame': centroprova_exame
    })

def exame_edit(request, pk):
    """
    View para Editar um Exame Realizado no Centro de Provas
    """
    # Obtém os filtros
    exame = get_object_or_404(CentroProvaExame, pk=pk)
    print(exame.data)
    alunos = Aluno.objects.order_by('nome')
    centrosprovas = CentroProva.objects.order_by('nome')
    certificacoes = Certificacao.objects.order_by('descricao')

    # Verifica se a requisição é do tipo POST (submissão de formulário)
    if request.method == "POST":
        form = CentroProvaExameForm(request.POST, instance=exame)

        # Se o formulário for válido, salva as alterações no objeto
        if form.is_valid():
            form.save()
            return redirect('exame_list')
    else:
        form = CentroProvaExameForm(instance=exame)

    # Renderização do template
    return render(request, 'centroProva/centroProva-exame_form.html', {
        'form': form, 
        'alunos': alunos,
        'centrosprovas': centrosprovas,
        'certificacoes': certificacoes
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
