from django.shortcuts import render, redirect, get_object_or_404

from .forms import ServicoForm
from .models import Servico


def home_view(request):
    return render(request, 'automecom/home.html')


def servico_list(request):
    servicos = Servico.objects.all()
    return render(request, 'automecom/home.html', {'servicos': servicos})


def servico_create(request):
    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('servico_list')
    else:
        form = ServicoForm()
    return render(request, 'automecom/home.html', {'form': form})


def servico_edit(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    if request.method == 'POST':
        form = ServicoForm(request.POST, instance=servico)
        if form.is_valid():
            form.save()
            return redirect('servico_list')
    else:
        form = ServicoForm(instance=servico)
    return render(request)
