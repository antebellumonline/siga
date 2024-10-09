from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.forms import inlineformset_factory
from django.urls import reverse
from .models import CentroProva, CentroProvaExame
from .forms import CentroProvaForm, CentroProvaExameForm

# View para a Página Inicial do Projeto
@login_required
def home(request):
    return render(request, 'home.html')

# View para a Página de Login
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

# View para a Página Inicial do Centro de Provas
def centroProva_home(request):
    return render(request, 'centroProva/centroProva_home.html')

# CRUD Centro de Provas
def centroProva_new(request):
    if request.method == 'POST':
        form = CentroProvaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('centroProva_list'))
    else:
        form = CentroProvaForm()
    return render(request, 'centroProva/centroProva_form.html', {'form': form})

def centroProva_list(request):
    query = request.GET.get('q')  # Obtém o termo de busca da URL
    inativo = request.GET.get('inativo')  # Obtém o filtro de status (inativo)

    # Ordenação
    order_by = request.GET.get('order_by', 'nome')  # Define a ordenação padrão por Nome
    descending = request.GET.get('descending', 'False') == 'True'  # Verifica se é para ordenar de forma descendente

    # Inicializa a variável centroProva
    centroProva = CentroProva.objects.all()

    # Aplicar os filtros e pesquisa
    if query:
        centroProva = centroProva.filter(nome__icontains=query)  # Pesquisa por nome (parcial)
    if inativo:
        centroProva = centroProva.filter(inativo=inativo)  # Filtra por status

    # Aplicar ordenação
    if descending:
        order_by = f'-{order_by}'
    centroProva = centroProva.order_by(order_by)

    return render(request, 'centroProva/centroProva_list.html', {'centroProva': centroProva})

def centroProva_detail(request, pk):
    centroProva = get_object_or_404(CentroProva, pk=pk)
    return render(request, 'centroProva/centroProva_detail.html', {'centroProva': centroProva})

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

def centroProva_delete(request, pk):
    centroProva = get_object_or_404(CentroProva, pk=pk)
    if request.method == "POST":
        centroProva.delete()
        return redirect('centroProva_list')
    return render(request, 'centroProva/centroProva_confirmDelete.html', {'centroProva': centroProva})

def centroProva_reports(request):
    # Placeholder para a funcionalidade de relatórios
    return render(request, 'centroProva/centroProva_reports.html')

# CRUD Exames
def exame_new(request):
    if request.method == 'POST':
        form = CentroProvaExameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('exame_list'))
    else:
        form = CentroProvaExameForm()
    return render(request, 'centroProva/centroProva-exame_form.html', {'form': form})

def exame_list(request):
    exames = CentroProvaExame.objects.all()
    return render(request, 'centroProva/centroProva-exame_list.html', {'exames': exames})

def exame_reports(request):
    # Placeholder para a funcionalidade de relatórios
    return render(request, 'centroProva/centroProva-exame_reports.html')
