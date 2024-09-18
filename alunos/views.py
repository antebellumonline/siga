# apps/alunos/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Aluno
from .forms import AlunoForm

def aluno_list(request):
    alunos = Aluno.objects.all()
    return render(request, 'alunos/aluno_list.html', {'alunos': alunos})

def aluno_detail(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    return render(request, 'alunos/aluno_detail.html', {'aluno': aluno})

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
