from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from automecom.templatetags.custom_tags import is_administrador
from .forms import ServicoForm, UtilizadorForm, UserForm, PasswordForm, RegisterForm, MarcacaoForm, VeiculoForm, \
    MarcacaoEditForm, MarcacaoEditFormClient
from .models import Servico, Utilizador, Veiculo, Marcacao
from django import template

register = template.Library()


def is_superuser(user):
    return user.is_superuser


def home_view(request):
    return render(request, 'automecom/home.html')


@login_required
def view_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('automecom:Home'))


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


def garantia_view(request):
    return render(request, 'automecom/garantia.html')


def privacidade_view(request):
    return render(request, 'automecom/privacidade.html')


def obras_view(request):
    utilizador = Utilizador.objects.get(user=request.user)
    context = {
        "marcacoes": Marcacao.objects.filter(utilizador_id=utilizador),
        "estado": Marcacao.estado,
        "data": Marcacao.data,
        "hora": Marcacao.hora,
    }
    if is_administrador(request.user):
        context = {
            "marcacoes": Marcacao.objects.all(),
            "estado": Marcacao.estado,
            "data": Marcacao.data,
            "hora": Marcacao.hora,
        }
    return render(request, 'automecom/obras.html', context)


def sobre_view(request):
    return render(request, 'automecom/sobre.html')


def marcacoes_view(request):
    utilizador = Utilizador.objects.get(user=request.user)
    context = {
        "marcacoes": Marcacao.objects.filter(utilizador_id=utilizador),
        "estado": Marcacao.estado,
        "descricao": Marcacao.descricao,
        "data": Marcacao.data,
        "hora": Marcacao.hora,
    }
    if is_administrador(request.user):
        context = {
            "marcacoes": Marcacao.objects.all(),
            "estado": Marcacao.estado,
            "descricao": Marcacao.descricao,
            "data": Marcacao.data,
            "hora": Marcacao.hora,
            "fatura": Marcacao.fatura,
        }
    return render(request, 'automecom/marcacoes.html', context)


def register_view(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'automecom/register.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username
            utilizador = Utilizador()
            utilizador.nome = user.username
            utilizador.user = user
            user.save()
            utilizador.save()
            login(request, user)
            return redirect('automecom:Home')
        else:
            return render(request, 'automecom/register.html', {'form': form})


def perfil_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('automecom:login'))

    post = Utilizador.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=request.user)
        form2 = UtilizadorForm(request.POST, request.FILES, instance=post)
        form3 = PasswordForm(request.user, request.POST)
        if form.is_valid():
            if form2.is_valid():
                if form3.is_valid():
                    form.save()
                    form2.save()
                    form3.save()
            return HttpResponseRedirect(reverse('automecom:perfil'))
    else:
        form = UserForm(instance=request.user)
        form2 = UtilizadorForm(instance=post)
        form3 = PasswordForm(request.user)
        context = {'form': form, 'form2': form2, 'form3': form3}
    return render(request, 'automecom/perfil.html', context)


@login_required
def utilizador_delete(request, post_id):
    if Utilizador.objects.filter(pk=post_id).exists():
        logout(request)
        Utilizador.objects.get(pk=post_id).user.delete()
    return HttpResponseRedirect(reverse('automecom:Home'))


def marcacao_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('automecom:login'))
    if request.method == 'GET':
        form = MarcacaoForm()
        form2 = VeiculoForm()
        if request.user.is_authenticated:
            del form.fields['nome']
            del form.fields['apelido']
            del form.fields['email']
        return render(request, 'automecom/marcacao.html', {'form': form, 'form2': form2})

    if request.method == 'POST':
        form = MarcacaoForm()
        form2 = VeiculoForm(request.POST)
        if form2.is_valid():
            if request.user.is_authenticated:

                veiculo = form2.save()
                marcacao = Marcacao(nome=request.user.first_name, apelido=request.user.last_name,
                                    email=request.user.email, telefone=request.POST['telefone'], veiculo=veiculo,
                                    data=request.POST['data'], hora=request.POST['hora'],
                                    descricao=request.POST['descricao'])
                utilizador = Utilizador.objects.get(user=request.user)
                marcacao.utilizador = utilizador
                marcacao.save()
            else:
                veiculo = form2.save()
                marcacao = Marcacao(nome=request.POST['nome'], apelido=request.POST['apelido'],
                                    email=request.POST['email'], telefone=request.POST['telefone'], veiculo=veiculo,
                                    data=request.POST['data'], hora=request.POST['hora'],
                                    descricao=request.POST['descricao'])
                marcacao.save()
            return redirect('automecom:marcacoes')
        else:
            return render(request, 'automecom/marcacao.html', {'form': form, 'form2': form2})


def marcacao_edit(request, post_id):
    post = Marcacao.objects.get(id=post_id)
    if not is_administrador(request.user) and post.utilizador.user != request.user:
        return HttpResponseRedirect(reverse('automecom:Home'))

    if request.method == 'POST':
        if is_administrador(request.user):
            form = MarcacaoEditForm(request.POST or None, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('automecom:marcacoes'))
        else:
            form = MarcacaoEditFormClient(request.POST or None, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('automecom:marcacoes'))
    else:
        if is_administrador(request.user):
            form = MarcacaoEditForm(instance=post)
        else:
            form = MarcacaoEditFormClient(instance=post)
        context = {'form': form, 'post_id': post_id}
        return render(request, 'automecom/editmarcacao.html', context)


def marcacao_delete(request, post_id):
    if Marcacao.objects.filter(pk=post_id).exists():
        Marcacao.objects.get(pk=post_id).delete()
    return HttpResponseRedirect(reverse('automecom:marcacoes'))
