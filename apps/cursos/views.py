# apps/cursos/views.py

"""
Definição das views para o aplicativo 'cursos'.

As views utilizam Django para gerenciar as requisições HTTP 
e interagir com os modelos de dados.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Q

from .models import Curso, CursoCategoria, CursoCertificacao
from .forms import CursoForm, CursoCategoriaForm, CursoCertificacaoForm

def curso_home(request):
    """
    View para a Página Inicial do App Cursos
    """
    return render(request, 'cursos/curso_home.html')

def cursocategoria_new(request):
    """
    View para Adicionar uma Categoria de Cursos
    """
    if request.method == 'POST':
        form = CursoCategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('cursoCategoria_list'))
    else:
        form = CursoCategoriaForm()
    return render(request, 'cursos/cursoCategoria_form.html', {
        'form': form
    })

def cursocategoria_list(request):
    """
    View para Listar as Categorias de Cursos    
    """
    # Obtém os filtros
    query = request.GET.get('q')
    inativo = request.GET.get('inativo')

    # Ordenação
    order_by = request.GET.get('order_by', 'nome')
    descending = request.GET.get('descending', 'False') == 'True'

    # Inicializa a variável cursoCategoria
    cursocategoria = CursoCategoria.objects.all()

    # Aplicar os filtros e pesquisa
    if query:
        cursocategoria = cursocategoria.filter(
            Q(id__icontains=query) |
            Q(nome__icontains=query) |
            Q(sigla__icontains=query)
        )

    # Filtra por Status
    if inativo is not None and inativo != "":
        if inativo == 'True':
            cursocategoria = cursocategoria.filter(inativo=True)
        elif inativo == 'False':
            cursocategoria = cursocategoria.filter(inativo=False)

    # Aplicar ordenação
    if descending:
        order_by = f'-{order_by}'
    cursocategoria = cursocategoria.order_by(order_by)

    # Quantidade de registros por página (com valor padrão de 20)
    records_per_page = request.GET.get('records_per_page', 20)
    try:
        records_per_page = int(records_per_page)
    except (ValueError, TypeError):
        records_per_page = 10

    # Criação do paginator com o queryset e o número de registros por página
    paginator = Paginator(cursocategoria, records_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Tratamento de erros para garantir que o objeto de página seja válido
    try:
        page_obj = paginator.get_page(page_number)
    except (ValueError, TypeError):
        page_obj = paginator.get_page(1)

    # Renderização do template
    return render(request, 'cursos/cursoCategoria_list.html', {
        'cursocategoria': cursocategoria,
        'page_obj': page_obj,
        'query_params': request.GET,
        })

def cursocategoria_detail(request, sigla):
    """
    View para Visualizar os detalhes de uma Categoria de Cursos   
    """
    # Obtém o objeto pelo ID (pk) ou retorna erro 404 se não encontrado
    cursocategoria = get_object_or_404(CursoCategoria, sigla=sigla)

    # Renderização do template
    return render(request, 'cursos/cursoCategoria_detail.html', {
        'cursocategoria': cursocategoria
    })

def cursocategoria_edit(request, sigla):
    """
    View para Editar uma Categoria de Cursos
    """
    # Obtém o objeto pelo ID (pk) ou retorna erro 404 se não encontrado
    cursocategoria = get_object_or_404(CursoCategoria, sigla=sigla)

    # Verifica se a requisição é do tipo POST (submissão de formulário)
    if request.method == "POST":
        form = CursoCategoriaForm(request.POST, instance=cursocategoria)

        # Se o formulário for válido, salva as alterações no objeto
        if form.is_valid():
            form.save()
            return redirect('cursoCategoria_list')
    else:
        form = CursoCategoriaForm(instance=cursocategoria)

    # Renderização do template
    return render(request, 'cursos/cursoCategoria_form.html', {
        'form': form
    })

def cursocategoria_delete(request, sigla):
    """
    View para Excluir uma Categoria de Cursos
    """
    cursocategoria = get_object_or_404(CursoCategoria, sigla=sigla)
    if request.method == "POST":
        cursocategoria.delete()
        return redirect('cursoCategoria_list')
    return render(request, 'cursos/cursoCategoria_confirmDelete.html', {
        'cursocategoria': cursocategoria
    })

# ----- XXXXX ----- XXXXX -----

def curso_new(request):
    """
    View para Adicionar um Curso
    """
    categorias = CursoCategoria.objects.filter(inativo=False).order_by('nome')
    if request.method == "POST":
        form = CursoForm(request.POST)
        formset = CursoCertificacaoForm(request.POST)
        if form.is_valid() and formset.is_valid():
            curso = form.save()
            formset.instance = curso
            formset.save()
            return redirect('curso_list')
    else:
        form = CursoForm()
        formset = CursoCertificacaoForm()
    return render(request, 'cursos/curso_form.html',{
        'form': form,
        'formset': formset,
        'categorias': categorias
    })

def curso_list(request):
    """
    View para Listar os Cursos
    """
    # Obtém os filtros
    query = request.GET.get('q')
    categoria = request.GET.get('cursoCategoria')
    inativo = request.GET.get('inativo')

    # Ordenação
    order_by = request.GET.get('order_by', 'nome')
    descending = request.GET.get('descending', 'False') == 'True'

    # Otimização de Consulta
    curso = Curso.objects.select_related(
        'cursoCategoria'
    )

    # Filtra por Categoria
    if categoria:
        curso = curso.filter(cursoCategoria__id=categoria)

    # Inicializa a variável curso
    curso = Curso.objects.all()

    # Aplicar os filtros e pesquisa
    if query:
        curso = curso.filter(
            Q(id__icontains=query) |
            Q(nome__icontains=query)
        )

    # Filtra por Status
    if inativo in ['True', 'False']:
        curso = curso.filter(inativo=inativo == 'True')

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

    # Buscar e ordenar opções de seleção
    categoria = CursoCategoria.objects.order_by('nome')

    return render(request, 'cursos/curso_list.html', {
        'curso': curso,
        'categoria': categoria,
        'page_obj': page_obj,
        'query_params': request.GET.urlencode(),
        })

def curso_detail(request, pk):
    """
    View para Visualizar os Detalhes de um Curso
    """
    # Obtém os filtros
    curso = get_object_or_404(Curso, pk=pk)
    certificacoes = CursoCertificacao.objects.filter(curso=curso).order_by('certificacao__descricao')

    # Renderização do template
    return render(request, 'cursos/curso_detail.html', {
        'curso': curso,
        'certificacoes': certificacoes
    })

def curso_edit(request, pk):
    """
    View para Editar um Curso
    """
    # Obtém os filtros
    curso = get_object_or_404(Curso, pk=pk)
    categorias = CursoCategoria.objects.filter(inativo=False).order_by('nome')

    # Verifica se a requisição é do tipo POST (submissão de formulário)
    if request.method == "POST":
        form = CursoForm(request.POST, instance=curso)
        formset = CursoCertificacaoForm(request.POST, instance=curso)

        # Se o formulário for válido, salva as alterações no objeto
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('curso_list')
        else:
            print(form.errors)
            for certificacao_form in formset:
                print(certificacao_form.errors)
    else:
        form = CursoForm(instance=curso)
        formset = CursoCertificacaoForm(instance=curso)

    # Renderização do template
    return render(request, 'cursos/curso_form.html', {
        'form': form,
        'formset': formset,
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
