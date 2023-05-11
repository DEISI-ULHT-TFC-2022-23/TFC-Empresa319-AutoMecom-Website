from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from automecom.templatetags.custom_tags import is_administrador
from .forms import ServicoForm
from .models import Servico, RegisterForm, Utilizador
from django import template

register = template.Library()


def is_superuser(user):
    return user.is_superuser


def home_view(request):
    return render(request, 'automecom/home.html')


def view_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('automecom:Home'))
        else:
            return render(request, 'automecom/login.html', {
                'message': 'Credenciais invalidas.'
            })

    return render(request, 'automecom/login.html')


def servico_view(request):
    servicos = Servico.objects.all()

    return render(request, 'automecom/servico.html',
                  {'servicos': servicos, 'administrador': is_administrador(request.user)})


def servico_create(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('automecom:login'))

    if not is_administrador(request.user):
        return HttpResponseRedirect(reverse('automecom:Home'))

    if request.method == 'POST':
        form = ServicoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('automecom:Servico'))
    form = ServicoForm()

    context = {'form': form}
    return render(request, 'automecom/create.html', context)


def servico_edit(request, post_id):
    if not is_administrador(request.user):
        return HttpResponseRedirect(reverse('automecom:Home'))

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


@login_required
def servico_delete(request, post_id):
    if Servico.objects.filter(pk=post_id).exists():
        Servico.objects.get(pk=post_id).delete()
    return HttpResponseRedirect(reverse('automecom:Servico'))


def conselho_view(request):
    return render(request, 'automecom/conselhos.html')


def contacto_view(request):
    return render(request, 'automecom/contactos.html')


def sobre_view(request):
    return render(request, 'automecom/sobre.html')


def marcacao_view(request):
    return render(request, 'automecom/marcacao.html')


def register_view(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'automecom/register.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            utilizador = Utilizador()
            utilizador.nome = user.username
            utilizador.user = user
            user.save()
            utilizador.save()
            login(request, user)
            return redirect('automecom:Home')
        else:
            return render(request, 'automecom/register.html', {'form': form})
