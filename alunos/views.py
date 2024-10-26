from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.forms import inlineformset_factory, modelformset_factory
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Aluno, AlunoContato
from cidades.models import Cidade, Estado
from .forms import AlunoForm

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

# ----- Definindo o formset para AlunoContato -----
AlunoContatoFormSet = inlineformset_factory(
    Aluno,
    AlunoContato, 
    fields=('tipoContato', 'contato', 'detalhe'),
    extra=1, 
    can_delete=True)

# ----- View para a Página Inicial de Alunos -----
def aluno_home(request):
    return render(request, 'alunos/aluno_home.html')

# ----- View para Adicionar um Aluno -----
def aluno_new(request):
    cidades = Cidade.objects.select_related('estado').order_by('nome')  # Ordenar por nome
    if request.method == "POST":
        form = AlunoForm(request.POST)
        formset = AlunoContatoFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            aluno = form.save()  # Salva o aluno
            formset.instance = aluno  # Define a instância do aluno no formset
            formset.save()  # Salva os contatos
            return redirect('aluno_list')
    else:
        form = AlunoForm()
        formset = AlunoContatoFormSet()
    return render(request, 'alunos/aluno_form.html', {'form': form, 'formset': formset, 'cidades': cidades})

# ----- View para Listar os Alunos -----
def aluno_list(request):
    # Obtém os filtros
    query = request.GET.get('q')  # Obtém o termo de busca da URL
    inativo = request.GET.get('inativo')  # Obtém o filtro de status (inativo)
    cidade = request.GET.get('cidade')  # Obtém o filtro de cidade

    # Ordenação
    order_by = request.GET.get('order_by', 'nome')  # Define a ordenação padrão por Nome
    descending = request.GET.get('descending', 'False') == 'True'  # Verifica se é para ordenar de forma descendente

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
        records_per_page = 10

    # Criação do paginator com o queryset e o número de registros por página
    paginator = Paginator(alunos, records_per_page)
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
    cidades = Cidade.objects.select_related('estado').all().order_by('nome')

    # Renderização do template
    return render(request, 'alunos/aluno_list.html', {
        'alunos': alunos,
        'page_obj': page_obj,
        'cidades': cidades,
        'query_params': request.GET,
    })

# ----- View para Visualizar os detalhes de um Alluno -----
def aluno_detail(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    contatos = AlunoContato.objects.filter(aluno=aluno)  # Aqui você busca os contatos relacionados ao aluno
    return render(request, 'alunos/aluno_detail.html', {'aluno': aluno, 'contatos': contatos})

# ----- View para Editar um Aluno -----
def aluno_edit(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    cidades = Cidade.objects.select_related('estado').order_by('nome')  # Ordenar por nome
    if request.method == "POST":
        form = AlunoForm(request.POST, instance=aluno)
        formset = AlunoContatoFormSet(request.POST, instance=aluno)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('aluno_list')
    else:
        form = AlunoForm(instance=aluno)
        formset = AlunoContatoFormSet(instance=aluno)
    return render(request, 'alunos/aluno_form.html', {'form': form, 'formset': formset, 'cidades': cidades})

# ----- View para Excluir um Aluno -----
def aluno_delete(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    if request.method == "POST":
        aluno.delete()
        return redirect('aluno_list')
    return render(request, 'alunos/aluno_confirm_delete.html', {'aluno': aluno})
