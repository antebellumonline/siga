# apps/instrutores/views.py

"""
Definição das views para o aplicativo 'instrutores'.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Q

from .models import Instrutor
from .forms import InstrutorForm

def instrutor_home(request):
    """
    View para a Página Inicial dos Instrutores
    """
    return render(request, 'instrutores/instrutor_home.html')

def instrutor_new(request):
    """
    View para Adicionar um Instrutor
    """
    if request.method == 'POST':
        form = InstrutorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('instrutor_list'))
    else:
        form = InstrutorForm()
    return render(request, 'instrutores/instrutor_form.html', {
        'form': form
    })

def instrutor_list(request):
    """
    View para Listar os Instrutores
    """
    # Obtém os filtros
    query = request.GET.get('q')
    inativo = request.GET.get('inativo')

    # Ordenação
    order_by = request.GET.get('order_by', 'nome')
    descending = request.GET.get('descending', 'True') == 'True'

    # Inicializa a variável instrutor
    instrutor = Instrutor.objects.all()

    # Aplicar os filtros e pesquisa
    if query:
        instrutor = instrutor.filter(
            Q(id__icontains=query) |
            Q(nome__icontains=query)
        )

    # Filtra por Status
    if inativo in ['True', 'False']:
        instrutor = instrutor.filter(inativo=inativo == 'True')

    # Aplicar ordenação
    if descending:
        order_by = f'-{order_by}'
    instrutor = instrutor.order_by(order_by)

    # Quantidade de registros por página (com valor padrão de 20)
    records_per_page = request.GET.get('records_per_page', 20)
    try:
        records_per_page = int(records_per_page)
    except (ValueError, TypeError):
        records_per_page = 20

    # Criação do paginator com o queryset e o número de registros por página
    paginator = Paginator(instrutor, records_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Tratamento de erros para garantir que o objeto de página seja válido
    try:
        page_obj = paginator.get_page(page_number)
    except (ValueError, TypeError):
        page_obj = paginator.get_page(1)

    context = {
        'instrutor': instrutor,
        'page_obj': page_obj,
        'query_params': request.GET.urlencode(),
        'headers': [
            {'field': 'id', 'label': 'ID'},
            {'field': 'nome', 'label': 'Nome do Instrutor'},
            {'field': 'inativo', 'label': 'Inativo'},
        ],
        'rows': [
            [
                instrutor.id,
                instrutor.nome,
                "Sim" if instrutor.inativo else "Não",
            ]
            for instrutor in page_obj
        ]
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'includes/table.html', context)
    else:
        return render(request, 'instrutores/instrutor_list.html', context)

def instrutor_detail(request, pk):
    """
    View para Visualizar os detalhes de um Instrutor  
    """
    # Obtém o objeto pelo ID (pk) ou retorna erro 404 se não encontrado
    instrutor = get_object_or_404(Instrutor, pk=pk)

    # Renderização do template
    return render(request, 'instrutores/instrutor_detail.html', {
        'instrutor': instrutor
    })

def instrutor_edit(request, pk):
    """
    View para Editar um Instrutor
    """
    # Obtém o objeto pelo ID (pk) ou retorna erro 404 se não encontrado
    instrutor = get_object_or_404(Instrutor, pk=pk)

    # Verifica se a requisição é do tipo POST (submissão de formulário)
    if request.method == "POST":
        form = InstrutorForm(request.POST, instance=instrutor)

        # Se o formulário for válido, salva as alterações no objeto
        if form.is_valid():
            form.save()
            return redirect('instrutor_list')
    else:
        form = InstrutorForm(instance=instrutor)

    # Renderização do template
    return render(request, 'instrutores/instrutor_form.html', {
        'form': form
    })

def instrutor_delete(request, pk):
    """
    View para Excluir um Instrutor
    """
    instrutor = get_object_or_404(Instrutor, pk=pk)
    if request.method == "POST":
        instrutor.delete()
        return redirect('instrutor_list')
    return render(request, 'instrutores/instrutor_confirmDelete.html', {
        'instrutor': instrutor
    })
