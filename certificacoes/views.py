from django.shortcuts import render, get_object_or_404, redirect
from .models import Certificacao, Certificador
from .forms import CertificacaoForm, CertificadorForm  # Certifique-se de criar esses formulários

# Página principal de certificadores
def certificador_home(request):
    return render(request, 'certificacoes/certificador_home.html')

# Listar Certificadores
def certificador_list(request):
    certificadores = Certificador.objects.all()
    return render(request, 'certificacoes/certificador_list.html', {'certificadores': certificadores})

# Detalhes do Certificador
def certificador_detail(request, pk):
    certificador = get_object_or_404(Certificador, pk=pk)
    return render(request, 'certificacoes/certificador_detail.html', {'certificador': certificador})

# Criar Certificador
def certificador_create(request):
    if request.method == "POST":
        form = CertificadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('certificador_list')
    else:
        form = CertificadorForm()
    return render(request, 'certificacoes/certificador_form.html', {'form': form})

# Atualizar Certificador
def certificador_update(request, pk):
    certificador = get_object_or_404(Certificador, pk=pk)
    if request.method == "POST":
        form = CertificadorForm(request.POST, instance=certificador)
        if form.is_valid():
            form.save()
            return redirect('certificador_list')
    else:
        form = CertificadorForm(instance=certificador)
    return render(request, 'certificacoes/certificador_form.html', {'form': form})

# Excluir Certificador
def certificador_delete(request, pk):
    certificador = get_object_or_404(Certificador, pk=pk)
    if request.method == "POST":
        certificador.delete()
        return redirect('certificador_list')
    return render(request, 'certificacoes/certificador_confirm_delete.html', {'certificador': certificador})

# Página principal de certificações
def certificacao_home(request):
    return render(request, 'certificacoes/certificacao_home.html')

# Listar Certificações
def certificacao_list(request):
    certificacoes = Certificacao.objects.all()
    return render(request, 'certificacoes/certificacao_list.html', {'certificacoes': certificacoes})

# Detalhes da Certificação
def certificacao_detail(request, pk):
    certificacao = get_object_or_404(Certificacao, pk=pk)
    return render(request, 'certificacoes/certificacao_detail.html', {'certificacao': certificacao})

# Criar Certificação
def certificacao_create(request):
    if request.method == "POST":
        form = CertificacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('certificacao_list')
    else:
        form = CertificacaoForm()
    return render(request, 'certificacoes/certificacao_form.html', {'form': form})

# Atualizar Certificação
def certificacao_update(request, pk):
    certificacao = get_object_or_404(Certificacao, pk=pk)
    if request.method == "POST":
        form = CertificacaoForm(request.POST, instance=certificacao)
        if form.is_valid():
            form.save()
            return redirect('certificacao_list')
    else:
        form = CertificacaoForm(instance=certificacao)
    return render(request, 'certificacoes/certificacao_form.html', {'form': form})

# Excluir Certificação
def certificacao_delete(request, pk):
    certificacao = get_object_or_404(Certificacao, pk=pk)
    if request.method == "POST":
        certificacao.delete()
        return redirect('certificacao_list')
    return render(request, 'certificacoes/certificacao_confirm_delete.html', {'certificacao': certificacao})
