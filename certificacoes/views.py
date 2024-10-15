from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Certificacao, Certificador
from .forms import CertificacaoForm, CertificadorForm  # Certifique-se de criar esses formulários

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

# Página principal de certificações
def certificacao_home(request):
    return render(request, 'certificacao/certificacao_home.html')

# Listar Certificadores
def certificador_list(request):
    query = request.GET.get('q')  # Obtém o termo de busca da URL
    inativo = request.GET.get('inativo')  # Obtém o filtro de status (inativo)

    # Ordenação
    order_by = request.GET.get('order_by', 'descricao')  # Define a ordenação padrão por Descrição
    descending = request.GET.get('descending', 'False') == 'True'  # Verifica se é para ordenar de forma descendente

    # Inicializa a variável certificador
    certificador = Certificador.objects.all()

    # Aplicar os filtros e pesquisa
    if query:
        certificador = certificador.filter(
            Q(descricao__icontains=query) | Q(siglaCertificador__icontains=query)
        ) # Pesquisa por descrição ou sigla (parcial)
    if inativo:
        # Converte o valor de 'inativo' para booleano
        inativo_value = inativo.lower() == 'true'
        certificador = certificador.filter(inativo=inativo_value)

    # Aplicar ordenação
    if descending:
        order_by = f'-{order_by}'
    certificador = certificador.order_by(order_by)

    # Paginação
    records_per_page = request.GET.get('records_per_page', 10)  # Padrão: 10 registros por página
    try:
        records_per_page = int(records_per_page) if records_per_page else 10
    except ValueError:
        records_per_page = 10
        
    paginator = Paginator(certificador, records_per_page)  # Cria o paginator

    page_number = request.GET.get('page')  # Obtém o número da página atual
    certificador_page = paginator.get_page(page_number)  # Pega a página solicitada

    return render(request, 'certificacao/certificador_list.html', {'certificador': certificador_page})

# Detalhes do Certificador
def certificador_detail(request, pk):
    certificador = get_object_or_404(Certificador, pk=pk)
    return render(request, 'certificacao/certificador_detail.html', {'certificador': certificador})

# Criar Certificador
def certificador_new(request):
    if request.method == "POST":
        form = CertificadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('certificador_list')
    else:
        form = CertificadorForm()
    return render(request, 'certificacao/certificador_form.html', {'form': form})

# Atualizar Certificador
def certificador_edit(request, pk):
    certificador = get_object_or_404(Certificador, pk=pk)
    if request.method == "POST":
        form = CertificadorForm(request.POST, instance=certificador)
        if form.is_valid():
            inativo_value = request.POST.get('inativo') == 'True'
            certificador.inativo = inativo_value
            certificador.save()
            return redirect('certificador_list')
    else:
        form = CertificadorForm(instance=certificador)
    return render(request, 'certificacao/certificador_form.html', {'form': form})

def certificador_delete(request, pk):
    certificador = get_object_or_404(Certificador, pk=pk)
    if request.method == "POST":
        certificador.delete()
        return JsonResponse({'success': True})  # Retorna um JSON de sucesso para a requisição AJAX
    else:
        # Para requisições GET, renderiza a página de confirmação
        return render(request, 'certificacao/certificador_confirm_delete.html', {'certificador': certificador})

# Listar Certificações
def certificacao_list(request):
    certificacoes = Certificacao.objects.all()
    return render(request, 'certificacao/certificacao_list.html', {'certificacoes': certificacoes})

# Detalhes da Certificação
def certificacao_detail(request, pk):
    certificacao = get_object_or_404(Certificacao, pk=pk)
    return render(request, 'certificacao/certificacao_detail.html', {'certificacao': certificacao})

# Criar Certificação
def certificacao_new(request):
    if request.method == "POST":
        form = CertificacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('certificacao_list')
    else:
        form = CertificacaoForm()
    return render(request, 'certificacao/certificacao_form.html', {'form': form})

# Atualizar Certificação
def certificacao_update(request, pk):
    certificacao = get_object_or_404(Certificacao, pk=pk)
    if request.method == "POST":
        form = CertificacaoForm(request.POST, instance=certificacao)
        if form.is_valid():
            form.save()
            return redirect('certificacao_list')
    else:
        form = CertificacaoForm(instance=certificacao)
    return render(request, 'certificacao/certificacao_form.html', {'form': form})

# Excluir Certificação
def certificacao_delete(request, pk):
    certificacao = get_object_or_404(Certificacao, pk=pk)
    if request.method == "POST":
        certificacao.delete()
        return redirect('certificacao_list')
    return render(request, 'certificacao/certificacao_confirm_delete.html', {'certificacao': certificacao})
