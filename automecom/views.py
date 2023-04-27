from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import ServicoForm
from .models import Servico


def home_view(request):
    return render(request, 'automecom/home.html')


def servico_view(request):
    servicos = Servico.objects.all()
    return render(request, 'automecom/servico.html', {'servicos': servicos})


def servico_create(request):
    if request.method == 'POST':
        form = ServicoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('automecom:Servico'))
    form = ServicoForm()
    context = {'form': form}
    return render(request, 'automecom/create.html', context)


def servico_edit(request, post_id):
    post = Servico.objects.get(id=post_id)
    if request.method == 'POST':
        form = ServicoForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('automecom:Servico'))
    else:
        form = ServicoForm(instance=post)
    context = {'form': form, 'post_id': post_id}
    return render(request, 'automecom/edit.html', context)


def servico_delete(request, post_id):
    if Servico.objects.filter(pk=post_id).exists():
        Servico.objects.get(pk=post_id).delete()
    return HttpResponseRedirect(reverse('automecom:Servico'))
