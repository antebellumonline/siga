from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from datetime import datetime
from django.urls import reverse
from django.db.models import Q
from .models import CentroProva, CentroProvaExame, Aluno, Certificacao
from .forms import CentroProvaForm, CentroProvaExameForm

# ----- View para a Página Inicial do Projeto -----
@login_required
def home(request):
    return render(request, 'home.html')

# ----- View para a Página de Login -----
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redireciona para a página inicial
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# ----- View para a Página Inicial do Centro de Provas -----
def centroProva_home(request):
    return render(request, 'centroProva/centroProva_home.html')

# ----- View para Adicionar um Centro de Provas -----
def centroProva_new(request):
    if request.method == 'POST':
        form = CentroProvaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('centroProva_list'))
    else:
        form = CentroProvaForm()
    return render(request, 'centroProva/centroProva_form.html', {'form': form})

# ----- View para Listar os Centros de Provas -----
def centroProva_list(request):
    # Obtém os filtros
    query = request.GET.get('q')  # Obtém o termo de busca da URL
    inativo = request.GET.get('inativo')  # Obtém o filtro de status (inativo)

    # Ordenação
    order_by = request.GET.get('order_by', 'nome')  # Define a ordenação padrão por Nome
    descending = request.GET.get('descending', 'False') == 'True'  # Verifica se é para ordenar de forma descendente

    # Inicializa a variável centroProva
    centroProva = CentroProva.objects.all()

    # Aplicar os filtros e pesquisa
    if query:
        centroProva = centroProva.filter(
            Q(id__icontains=query) |
            Q(nome__icontains=query)
        )
    
    # Filtra por Status
    if inativo is not None and inativo != "":  # Verifica se o filtro foi aplicado
        if inativo == 'True':
            centroProva = centroProva.filter(inativo=True)
        elif inativo == 'False':
            centroProva = centroProva.filter(inativo=False)

    # Aplicar ordenação
    if descending:
        order_by = f'-{order_by}'
    centroProva = centroProva.order_by(order_by)

    # Quantidade de registros por página (com valor padrão de 20)
    records_per_page = request.GET.get('records_per_page', 20)
    try:
        records_per_page = int(records_per_page)
    except (ValueError, TypeError):
        records_per_page = 10
        
    # Criação do paginator com o queryset e o número de registros por página
    paginator = Paginator(centroProva, records_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Tratamento de erros para garantir que o objeto de página seja válido
    try:
        page_obj = paginator.get_page(page_number)
    except (ValueError, TypeError):
        page_obj = paginator.get_page(1)  # Volta para a primeira página se o número de página for inválido

    # Renderização do template com o objeto de paginação e os parâmetros de consulta
    context = {
        'page_obj': page_obj,  # Objeto de paginação para uso no template
        'query_params': request.GET.urlencode()  # Parâmetros da URL para preservar na paginação
    }

    # Renderização do template
    return render(request, 'centroProva/centroProva_list.html', {
        'centroProva': centroProva,
        'page_obj': page_obj,
        'query_params': request.GET,
        })

# ----- View para Visualizar os detalhes de um Centro de Provas -----
def centroProva_detail(request, pk):
    # Obtém os filtros
    centroProva = get_object_or_404(CentroProva, pk=pk)

    # Renderização do template
    return render(request, 'centroProva/centroProva_detail.html', {
        'centroProva': centroProva
    })

# ----- View para Editar um Centro de Provas -----
def centroProva_edit(request, pk):
    centroProva = get_object_or_404(CentroProva, pk=pk)
    if request.method == "POST":
        form = CentroProvaForm(request.POST, instance=centroProva)
        if form.is_valid():
            form.save()
            return redirect('centroProva_list')
    else:
        form = CentroProvaForm(instance=centroProva)
    return render(request, 'centroProva/centroProva_form.html', {'form': form})

# ----- View para Excluir um Centro de Provas -----
def centroProva_delete(request, pk):
    centroProva = get_object_or_404(CentroProva, pk=pk)
    if request.method == "POST":
        centroProva.delete()
        return redirect('centroProva_list')
    return render(request, 'centroProva/centroProva_confirmDelete.html', {'centroProva': centroProva})

# ----- XXXXX ----- XXXXX -----

# ----- View para Adicionar um Exame Realizado no Centro de Provas -----
def exame_new(request):
    alunos = Aluno.objects.order_by('nome')
    centrosProvas = CentroProva.objects.order_by('nome')
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
    
    return render(
        request,
        'centroProva/centroProva-exame_form.html',
        {
            'form': form, 
            'alunos': alunos,
            'centrosProvas': centrosProvas,
            'certificacoes': certificacoes
        }
    )

# ----- View para Listar os Exames Realizados no Centro de Provas -----
def exame_list(request):
    # Obtém os filtros
    query = request.GET.get('q')
    data_range = request.GET.get('daterange')  # Intervalo de datas
    presenca = request.GET.get('presenca')  # Filtro por Presença
    cancelado = request.GET.get('cancelado')  # Filtro de Exame Cancelado
    centroProva = request.GET.get('centroProva')  # Filtro de Centro de Provas
    certificacao = request.GET.get('certificacao')  # Filtro de Certificação

    # Ordenação
    order_by = request.GET.get('order_by', 'data')  # Define a ordenação padrão por Data
    descending = request.GET.get('descending', 'False') == 'True'  # Verifica se é para ordenar de forma descendente

    # Otimização de Consulta
    centroProva_exame = CentroProvaExame.objects.select_related('aluno', 'centroProva', 'certificacao')

    # Aplicar os filtros e pesquisa
    if query:
        centroProva_exame = centroProva_exame.filter(
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
            centroProva_exame = centroProva_exame.filter(data__range=[data_inicio, data_fim])
        except (ValueError, TypeError):
            pass  # Ignorar filtro em caso de erro
    
    # Filtra por Presença
    if presenca in ['True', 'False']:
        centroProva_exame = centroProva_exame.filter(presenca=(presenca == 'True'))

    # Filtra por Cancelado
    if cancelado in ['True', 'False']:
        centroProva_exame = centroProva_exame.filter(cancelado=(cancelado == 'True'))

    # Filtra por Centro de Prova
    if centroProva:
        centroProva_exame = centroProva_exame.filter(centroProva__id=centroProva)
    
    # Filtra por Certificação
    if certificacao:
        centroProva_exame = centroProva_exame.filter(certificacao__id=certificacao)

    # Aplicar ordenação
    if descending:
        order_by = f'-{order_by}'
    centroProva_exame = centroProva_exame.order_by(order_by)

    # Quantidade de registros por página (com valor padrão de 20)
    records_per_page = request.GET.get('records_per_page', 20)
    try:
        records_per_page = int(records_per_page)
    except (ValueError, TypeError):
        records_per_page = 20

    # Criação do paginator com o queryset e o número de registros por página
    paginator = Paginator(centroProva_exame, records_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Tratamento de erros para garantir que o objeto de página seja válido
    try:
        page_obj = paginator.get_page(page_number)
    except (ValueError, TypeError):
        page_obj = paginator.get_page(1)  # Volta para a primeira página se o número de página for inválido

    # Renderização do template com o objeto de paginação e os parâmetros de consulta
    context = {
        'page_obj': page_obj,  # Objeto de paginação para uso no template
        'query_params': request.GET.urlencode()  # Parâmetros da URL para preservar na paginação
    }

    # Buscar e ordenar opções de seleção
    alunos = Aluno.objects.order_by('nome')
    centrosProva = CentroProva.objects.order_by('nome')
    certificacoes = Certificacao.objects.order_by('descricao')

    return render(request, 'centroProva/centroProva-exame_list.html', {
        'centroProva_exame': centroProva_exame,
        'page_obj': page_obj,
        'aluno': alunos,
        'centroProva': centrosProva,
        'certificacao': certificacoes,
        'query_params': request.GET.urlencode(),
    })

# ----- View para Visualizar os Detalhes de um Exame Realizado no Centro de Provas -----
def exame_detail(request, pk):
    centroProva_exame = get_object_or_404(CentroProvaExame, pk=pk)
    return render(request, 'centroProva/centroProva-exame_detail.html', {'centroProva_exame': centroProva_exame})

# ----- View para Editar um Exame Realizado no Centro de Provas -----
def exame_edit(request, pk):
    exame = get_object_or_404(CentroProvaExame, pk=pk)
    print(exame.data)
    alunos = Aluno.objects.order_by('nome')
    centrosProvas = CentroProva.objects.order_by('nome')
    certificacoes = Certificacao.objects.order_by('descricao')

    if request.method == "POST":
         form = CentroProvaExameForm(request.POST, instance=exame)
         if form.is_valid():
             form.save()
             return redirect('exame_list')
    else:
        form = CentroProvaExameForm(instance=exame)

    return render(
        request,
        'centroProva/centroProva-exame_form.html',
        {
            'form': form, 
            'alunos': alunos,
            'centrosProvas': centrosProvas,
            'certificacoes': certificacoes
        }
    )

# ----- View para Excluir um Centro de Provas -----
def exame_delete(request, pk):
    exame = get_object_or_404(CentroProvaExame, pk=pk)

    if request.method == "POST":
        exame.delete()
        return redirect('exame_list')
    
    return render(request, 'centroProva/centroProva-exame_confirm_delete.html', {'exame': exame})
