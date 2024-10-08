from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import CentroProva, CentroProvaExame
from .forms import CentroProvaForm, CentroProvaExameForm

# Página inicial com opções
def home(request):
    return render(request, 'centroprovas/home.html')

# CRUD Centro de Provas
def centro_prova_novo(request):
    if request.method == 'POST':
        form = CentroProvaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('centro_prova_localizar'))
    else:
        form = CentroProvaForm()
    return render(request, 'centroprovas/centro_prova_form.html', {'form': form})

def centro_prova_localizar(request):
    centros_prova = CentroProva.objects.all()
    return render(request, 'centroprovas/centro_prova_lista.html', {'centros_prova': centros_prova})

def centro_prova_relatorios(request):
    # Placeholder para a funcionalidade de relatórios
    return render(request, 'centroprovas/centro_prova_relatorios.html')

# CRUD Exames
def exame_novo(request):
    if request.method == 'POST':
        form = CentroProvaExameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('exame_localizar'))
    else:
        form = CentroProvaExameForm()
    return render(request, 'centroprovas/exame_form.html', {'form': form})

def exame_localizar(request):
    exames = CentroProvaExame.objects.all()
    return render(request, 'centroprovas/exame_lista.html', {'exames': exames})

def exame_relatorios(request):
    # Placeholder para a funcionalidade de relatórios
    return render(request, 'centroprovas/exame_relatorios.html')
