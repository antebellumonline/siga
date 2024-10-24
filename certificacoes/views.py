from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Certificacao, Certificador
from .forms import CertificacaoForm, CertificadorForm

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

# ----- View para a Página Inicial das Certificações -----
def certificacao_home(request):
    return render(request, 'certificacao/certificacao_home.html')

# ----- View para Adicionar um Certificador -----
def certificador_new(request):
    if request.method == "POST":
        form = CertificadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('certificador_list')
    else:
        form = CertificadorForm()
    return render(request, 'certificacao/certificador_form.html', {'form': form})

# ----- View para Listar os Certificadores -----
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

    return render(request, 'certificacao/certificador_list.html', {
        'certificador': certificador_page,
        'page-number': page_number,
        'query_params': request.GET,
        })

# ----- View para Visualizar os detalhes de um Certificador -----
def certificador_detail(request, pk):
    certificador = get_object_or_404(Certificador, pk=pk)
    return render(request, 'certificacao/certificador_detail.html', {'certificador': certificador})

# ----- View para Editar um Certificador -----
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

# ----- View para Excluir um Certificador -----
def certificador_delete(request, pk):
    certificador = get_object_or_404(Certificador, pk=pk)
    if request.method == "POST":
        certificador.delete()
        return JsonResponse({'success': True})
    else:
        return render(request, 'certificacao/certificador_confirm_delete.html', {'certificador': certificador})
    
# ----- XXXXX ----- XXXXX -----

# ----- View para Adicionar uma Certificação -----
def certificacao_new(request):
    certificadores = Certificador.objects.order_by('descricao')
    if request.method == "POST":
        form = CertificacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('certificacao_list')
        else:
            print(form.errors)
    else:
        form = CertificacaoForm()

    return render(request, 'certificacao/certificacao_form.html', {'form': form, 'certificadores': certificadores})

# ----- View para Listar as Certificações -----
def certificacao_list(request):
    query = request.GET.get('q')  # Obtém o termo de busca da URL

    # Ordenação
    order_by = request.GET.get('order_by', 'descricao')  # Define a ordenação padrão por Descrição
    descending = request.GET.get('descending', 'False') == 'True'  # Verifica se é para ordenar de forma descendente

    # Inicializa a variável certificacoes com select_related para otimizar a consulta
    certificacoes = Certificacao.objects.select_related('idCertificador').all()

    # Aplicar os filtros e pesquisa
    if query:
        certificacoes = certificacoes.filter(
            Q(descricao__icontains=query) | Q(siglaExame__icontains=query) |
            Q(idCertificador__descricao__icontains=query)
        )  # Pesquisa por descrição, sigla ou descrição do certificador (parcial)

    # Aplicar ordenação
    if descending:
        order_by = f'-{order_by}'
    certificacoes = certificacoes.order_by(order_by)

    # Paginação
    records_per_page = request.GET.get('records_per_page', 10)  # Padrão: 10 registros por página
    try:
        records_per_page = int(records_per_page) if records_per_page else 10
    except ValueError:
        records_per_page = 10

    paginator = Paginator(certificacoes, records_per_page)  # Cria o paginator

    page_number = request.GET.get('page')  # Obtém o número da página atual
    certificacoes_page = paginator.get_page(page_number)  # Pega a página solicitada

    return render(request, 'certificacao/certificacao_list.html', {
        'certificacoes': certificacoes_page,
        'page_number': page_number,  # Adiciona o número da página ao contexto
        'query_params': request.GET,  # Adiciona os parâmetros da query
    })

# ----- View para Visualizar os detalhes de uma Certificação -----
def certificacao_detail(request, pk):
    certificacao = get_object_or_404(Certificacao, id=pk)
    return render(request, 'certificacao/certificacao_detail.html', {'certificacao': certificacao})

# ----- View para Editar uma Certificação -----
def certificacao_edit(request, pk):
    certificacao = get_object_or_404(Certificacao, pk=pk)
    certificadores = Certificador.objects.order_by('descricao')
    if request.method == "POST":
        form = CertificacaoForm(request.POST, instance=certificacao)
        if form.is_valid():
            form.save()
            return redirect('certificacao_list')
    else:
        form = CertificacaoForm(instance=certificacao)
    return render(request, 'certificacao/certificacao_form.html', {'form': form, 'certificadores': certificadores})

# ----- View para Excluir uma Certificação -----
def certificacao_delete(request, pk):
    certificacao = get_object_or_404(Certificacao, pk=pk)
    if request.method == "POST":
        certificacao.delete()
        return redirect('certificacao_list')
    return render(request, 'certificacao/certificacao_confirm_delete.html', {'certificacao': certificacao})
