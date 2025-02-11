# apps/cursos/views.py

"""
Definição das views para o aplicativo 'centroProva'.

As views utilizam Django para gerenciar as requisições HTTP 
e interagir com os modelos de dados.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Curso, CursoCategoria
from .forms import CursoForm

def curso_home(request):
    """
    View para a Página Inicial do App Cursos
    """
    return render(request, 'cursos/curso_home.html')

def curso_new(request):
    """
    View para Adicionar um Curso
    """
    categorias = CursoCategoria.objects.filter(inativo=False).order_by('nome')
    if request.method == "POST":
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('curso_list')
    else:
        form = CursoForm()
    return render(request, 'cursos/curso_form.html',{
        'form': form,
        'categorias': categorias
    })

def curso_list(request):
    """
    View para Listar os Cursos
    """
    # Obtém os filtros
    query = request.GET.get('q')
    categoria = request.GET.get('categoria')
    inativo = request.GET.get('inativo')

    # Ordenação
    order_by = request.GET.get('order_by', 'nome')
    descending = request.GET.get('descending', 'False') == 'True'

    # Otimização de Consulta
    curso = Curso.objects.select_related(
        'categoria'
    )

    # Filtra por Aluno
    if categoria:
        curso = curso.filter(aluno__uid=aluno)

    # Inicializa a variável certificador
    curso = Curso.objects.all()

    # Aplicar os filtros e pesquisa
    if query:
        curso = curso.filter(
            Q(id__icontains=query) |
            Q(nome__icontains=query)
        )

    # Filtra por Status
    if inativo in ['True', 'False']:
        curso = curso.filter(inativo=(inativo == 'True'))

    # Aplicar ordenação
    if descending:
        order_by = f'-{order_by}'
    curso = curso.order_by(order_by)

    # Quantidade de registros por página (com valor padrão de 20)
    records_per_page = request.GET.get('records_per_page', 20)
    try:
        records_per_page = int(records_per_page)
    except (ValueError, TypeError):
        records_per_page = 20

    # Criação do paginator com o queryset e o número de registros por página
    paginator = Paginator(curso, records_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Tratamento de erros para garantir que o objeto de página seja válido
    try:
        page_obj = paginator.get_page(page_number)
    except (ValueError, TypeError):
        page_obj = paginator.get_page(1)

    # Renderização do template com o objeto de paginação e os parâmetros de consulta
    context = {
        'page_obj': page_obj,
        'query_params': request.GET.urlencode()
    }

    return render(request, 'cursos/curso_list.html', {
        'curso': curso,
        'page_obj': page_obj,
        'query_params': request.GET.urlencode(),
        })

def curso_detail(request, pk):
    """
    View para Visualizar os Detalhes de um Curso
    """
    # Obtém o objeto pelo ID (pk) ou retorna erro 404 se não encontrado
    curso = get_object_or_404(Curso, pk=pk)

    # Renderização do template
    return render(request, 'cursos/curso.html', {
        'curso': curso
    })

def curso_edit(request, pk):
    """
    View para Editar um Curso
    """
    # Obtém os filtros
    curso = get_object_or_404(Curso, pk=pk)
    print(curso.nome)
    categorias = CursoCategoria.objects.filter(inativo=False).order_by('nome')

    # Verifica se a requisição é do tipo POST (submissão de formulário)
    if request.method == "POST":
        form = CursoForm(request.POST, instance=curso)

        # Se o formulário for válido, salva as alterações no objeto
        if form.is_valid():
            form.save()
            return redirect('curso_list')
    else:
        form = CursoForm(instance=curso)

    # Renderização do template
    return render(request, 'cursos/curso_form.html', {
        'form': form, 
        'categorias': categorias
    })

def curso_delete(request, pk):
    """
    View para Excluir um Curso
    """
    curso = get_object_or_404(Curso, pk=pk)

    if request.method == "POST":
        curso.delete()
        return redirect('curso_list')

    return render(request, 'cursos/curso_confirm_delete.html', {
        'curso': curso
    })
