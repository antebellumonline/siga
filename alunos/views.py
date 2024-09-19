from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Aluno, AlunoContato
from .forms import AlunoForm

def aluno_list(request):
    query = request.GET.get('q')  # Obtém o termo de busca da URL
    inativo = request.GET.get('inativo')  # Obtém o filtro de status (inativo)

    # Ordenação
    order_by = request.GET.get('order_by', 'uid')  # Define a ordenação padrão por UID
    descending = request.GET.get('descending', 'False') == 'True'  # Verifica se é para ordenar de forma descendente

    # Otimiza a consulta usando select_related para carregar cidade junto com aluno
    alunos = Aluno.objects.select_related('cidade').all()

    # Aplicar os filtros e pesquisa
    if query:
        alunos = alunos.filter(nome__icontains=query)  # Pesquisa por nome (parcial)
    
    if inativo:
        alunos = alunos.filter(inativo=inativo)  # Filtra por status

    # Aplicar ordenação
    if descending:
        order_by = f'-{order_by}'
    alunos = alunos.order_by(order_by)

    return render(request, 'alunos/aluno_list.html', {'alunos': alunos})

def aluno_detail(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    contatos = AlunoContato.objects.filter(aluno=aluno)  # Aqui você busca os contatos relacionados ao aluno
    return render(request, 'alunos/aluno_detail.html', {'aluno': aluno, 'contatos': contatos})

def aluno_create(request):
    if request.method == "POST":
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('aluno_list')
    else:
        form = AlunoForm()
    return render(request, 'alunos/aluno_form.html', {'form': form})

def aluno_update(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    if request.method == "POST":
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            return redirect('aluno_list')
    else:
        form = AlunoForm(instance=aluno)
    return render(request, 'alunos/aluno_form.html', {'form': form})

def aluno_delete(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    if request.method == "POST":
        aluno.delete()
        return redirect('aluno_list')
    return render(request, 'alunos/aluno_confirm_delete.html', {'aluno': aluno})

def cidade_por_codigo_ibge(request, codigo_ibge):
    try:
        cidade = Cidade.objects.get(codigo_ibge=codigo_ibge)
        return JsonResponse({'cidade_id': cidade.id})
    except Cidade.DoesNotExist:
        return JsonResponse({'erro': 'Cidade não encontrada'}, status=404)
