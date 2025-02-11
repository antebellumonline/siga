# apps/certificacoes/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Certificacao, Certificador
from .forms import CertificacaoForm, CertificadorForm

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
    # Obtém os filtros
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
            Q(id__icontains=query) |
            Q(descricao__icontains=query) |
            Q(siglaCertificador__icontains=query)
        )
    
    # Filtra por Status
    if inativo in ['True', 'False']:
        certificador = certificador.filter(inativo=(inativo == 'True'))

    # Aplicar ordenação
    if descending:
        order_by = f'-{order_by}'
    certificador = certificador.order_by(order_by)

    # Quantidade de registros por página (com valor padrão de 20)
    records_per_page = request.GET.get('records_per_page', 20)
    try:
        records_per_page = int(records_per_page)
    except (ValueError, TypeError):
        records_per_page = 20
        
    # Criação do paginator com o queryset e o número de registros por página
    paginator = Paginator(certificador, records_per_page)
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

    return render(request, 'certificacao/certificador_list.html', {
        'certificador': certificador,
        'page_obj': page_obj,
        'query_params': request.GET.urlencode(),
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
    #Obtém os filtros
    query = request.GET.get('q')  # Obtém o termo de busca da URL
    certificador = request.GET.get('certificador')  # Filtro de Certificador
    inativo = request.GET.get('inativo')  # Obtém o filtro de status (inativo)

    # Ordenação
    order_by = request.GET.get('order_by', 'descricao')  # Define a ordenação padrão por Descrição
    descending = request.GET.get('descending', 'False') == 'True'  # Verifica se é para ordenar de forma descendente

    # Otimização de Consulta
    certificacao = Certificacao.objects.select_related('idCertificador')

    # Aplicar os filtros e pesquisa
    if query:
        certificacao = certificacao.filter(
            Q(id__icontains=query) |
            Q(descricao__icontains=query) |
            Q(siglaExame__icontains=query)
        )
    # Filtra por Status
    if inativo in ['True', 'False']:
        certificacao = certificacao.filter(inativo=(inativo == 'True'))

    # Filtra por Certificador
    if certificador:
        certificacao = certificacao.filter(idCertificador=certificador)

    # Aplicar ordenação
    if descending:
        order_by = f'-{order_by}'
    certificacao = certificacao.order_by(order_by)

    # Quantidade de registros por página (com valor padrão de 20)
    records_per_page = request.GET.get('records_per_page', 20)
    try:
        records_per_page = int(records_per_page)
    except (ValueError, TypeError):
        records_per_page = 10
        
    # Criação do paginator com o queryset e o número de registros por página
    paginator = Paginator(certificacao, records_per_page)
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
    certificador = Certificador.objects.order_by('descricao')

    # Renderização do template
    return render(request, 'certificacao/certificacao_list.html', {
        'certificacao': certificacao,
        'certificador': certificador,
        'page_obj': page_obj,
        'query_params': request.GET,
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
