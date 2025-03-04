# apps/empresas/views.py

"""
Definição das views para o aplicativo 'empresas'.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Q

from django.utils.safestring import mark_safe

from .models import Empresa, EmpresaContato, Cidade
from .forms import EmpresaForm, EmpresaContatoFormSet

def empresa_home(request):
    """
    View para a Página Inicial das Empresas
    """
    return render(request, 'empresas/empresa_home.html')

def empresa_new(request):
    """
    View para Adicionar uma Empresa
    """
    cidades = Cidade.objects.select_related('estado').order_by('nome')

    if request.method == "POST":
        form = EmpresaForm(request.POST)
        formset = EmpresaContatoFormSet(request.POST)

        if form.is_valid():
            empresa = form.save()  # Salva a empresa primeiro
            formset.instance = empresa  # Associa a empresa ao formset

            if formset.is_valid():
                formset.save()  # Salva os contatos
                return redirect('empresa_list')
            else:
                print("Erros no Formset:")
                for contato_form in formset:
                    print(contato_form.errors)  # Verifica erros no formset
        else:
            print("Erros no Formulário de Empresa:")
            print(form.errors)  # Verifica erros no formulário de empresa

    else:
        form = EmpresaForm()
        formset = EmpresaContatoFormSet()

    return render(request, 'empresas/empresa_form.html', {
        'form': form,
        'formset': formset,
        'cidades': cidades
    })

def empresa_list(request):
    """
    View para Listar as Empresas
    """
    # Obtém os filtros
    query = request.GET.get('q')
    cidade = request.GET.get('cidade')
    inativo = request.GET.get('inativo')

    # Ordenação
    order_by = request.GET.get('order_by', 'razaoSocial')
    descending = request.GET.get('descending', 'False') == 'True'

    # Otimiza a consulta usando select_related para carregar cidade junto com empresa
    empresas = Empresa.objects.all()

    # Otimização de Consulta
    empresas = Empresa.objects.select_related(
        'cidade',
    )

    # Aplicar os filtros e pesquisa
    if query:
        empresas = empresas.filter(
            Q(taxId__icontains=query) |
            Q(razaoSocial__icontains=query) |
            Q(fantasia__icontains=query) |
            Q(contatos__contato__icontains=query) |
            Q(contatos__detalhe__icontains=query)
        ).distinct()

    # Filtra por Cidade
    if cidade:
        empresas = empresas.filter(cidade__id=cidade)

    # Filtra por Status
    if inativo is not None and inativo != "":
        if inativo == 'True':
            empresas = empresas.filter(inativo=True)
        elif inativo == 'False':
            empresas = empresas.filter(inativo=False)

    # Aplicar ordenação
    if descending:
        order_by = f'-{order_by}'
    empresas = empresas.order_by(order_by)

    # Quantidade de registros por página (com valor padrão de 20)
    records_per_page = request.GET.get('records_per_page', 20)
    try:
        records_per_page = int(records_per_page)
    except (ValueError, TypeError):
        records_per_page = 20

    # Criação do paginator com o queryset e o número de registros por página
    paginator = Paginator(empresas, records_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Tratamento de erros para garantir que o objeto de página seja válido
    try:
        page_obj = paginator.get_page(page_number)
    except (ValueError, TypeError):
        page_obj = paginator.get_page(1)

    # Buscar e ordenar opções de seleção
    cidades = Cidade.objects.select_related('estado').all().order_by('nome')

    # Renderização do template
    context = {
        'empresas': empresas,
        'page_obj': page_obj,
        'cidades': cidades,
        'query_params': request.GET.urlencode(),
        'headers': [
            {'field': 'taxId', 'label': 'Tax ID (CNPJ)'},
            {'field': 'razaoSocial', 'label': 'Razão Social'},
            {'field': 'fantasia', 'label': 'Nome Fantasia'},
            {'field': 'cidade_nome', 'label': 'Cidade/UF'},
            {'field': 'inativo', 'label': 'Inativo'},
        ],
        'rows': [
            [
                empresa.taxId,
                mark_safe(f'<a href="{reverse(
                    "empresa_detail", args=[empresa.pk])}">{empresa.razaoSocial}</a>'),
                empresa.fantasia,
                f"{empresa.cidade.nome if empresa.cidade else '-'} / {empresa.cidade.estado.uf if empresa.cidade else '-'}",
                "Sim" if empresa.inativo else "Não",
            ] for empresa in page_obj
        ],
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'includes/table.html', context)
    else:
        return render(
            request,
            'empresas/empresa_list.html',
            context
    )

def empresa_detail(request, pk):
    """
    View para Visualizar os detalhes de uma Empresa
    """
    # Obtém os filtros
    empresa = get_object_or_404(Empresa, pk=pk)
    contatos = EmpresaContato.objects.filter(empresa=empresa).order_by('tipoContato__descricao')

    # Renderização do template
    return render(request, 'empresas/empresa_detail.html', {
        'empresa': empresa,
        'contatos': contatos
    })

def empresa_edit(request, pk):
    """
    View para Editar uma Empresa
    """
    empresa = get_object_or_404(Empresa, pk=pk)
    cidades = Cidade.objects.select_related('estado').order_by('nome')

    if request.method == "POST":
        form = EmpresaForm(request.POST, instance=empresa)
        formset = EmpresaContatoFormSet(request.POST, instance=empresa)

        print(request.POST)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('empresa_list')
        else:
            print(form.errors)
            for contato_form in formset:
                print(contato_form.errors)
    else:
        form = EmpresaForm(instance=empresa)
        formset = EmpresaContatoFormSet(instance=empresa)

    return render(request, 'empresas/empresa_form.html', {
        'form': form,
        'formset': formset,
        'cidades': cidades
    })

def empresa_delete(request, pk):
    """
    View para Excluir uma Empresa
    """
    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == "POST":
        empresa.delete()
        return redirect('empresa_list')
    return render(request, 'empresas/empresa_confirm_delete.html', {
        'empresa': empresa
    })
