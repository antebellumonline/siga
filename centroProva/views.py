from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import CentroProva, CentroProvaExame
from .forms import CentroProvaForm, CentroProvaExameForm

# Página inicial com opções
def centroProva_home(request):
    return render(request, 'centroProva/centroProva_home.html')

# CRUD Centro de Provas
def centroProva_new(request):
    if request.method == 'POST':
        form = CentroProvaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('centroProva_list'))
    else:
        form = CentroProvaForm()
    return render(request, 'centroProva/centroProva_form.html', {'form': form})

def centroProva_list(request):
    centros_prova = CentroProva.objects.all()
    return render(request, 'centroProva/centroProva_list.html', {'centros_prova': centros_prova})

def centroProva_reports(request):
    # Placeholder para a funcionalidade de relatórios
    return render(request, 'centroProva/centroProva_reports.html')

# CRUD Exames
def exame_new(request):
    if request.method == 'POST':
        form = CentroProvaExameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('exame_list'))
    else:
        form = CentroProvaExameForm()
    return render(request, 'centroProva/centroProva-exame_form.html', {'form': form})

def exame_list(request):
    exames = CentroProvaExame.objects.all()
    return render(request, 'centroProva/centroProva-exame_list.html', {'exames': exames})

def exame_reports(request):
    # Placeholder para a funcionalidade de relatórios
    return render(request, 'centroProva/centroProva-exame_reports.html')
