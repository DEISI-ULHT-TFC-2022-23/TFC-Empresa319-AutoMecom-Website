from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

from .models import Servico, Utilizador, Veiculo, Marcacao
from .widget import DatePickerInput, TimePickerInput


class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['nome', 'descricao']


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class UtilizadorForm(forms.ModelForm):
    class Meta:
        model = Utilizador
        fields = []


class PasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['placeholder'] = 'Senha atual'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Nova senha'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirme a nova senha'


class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['marca', 'modelo', 'ano', 'matricula']


class MarcacaoForm(forms.Form):
    nome = forms.CharField(max_length=200)
    apelido = forms.CharField(max_length=200)
    email = forms.CharField(max_length=200)
    servicos = forms.ModelMultipleChoiceField(queryset=Servico.objects.all())
    telefone = forms.IntegerField()
    descricao = forms.CharField(max_length=500)
    data = forms.DateField(widget=DatePickerInput)
    hora = forms.TimeField(widget=TimePickerInput)


class MarcacaoEditForm(forms.ModelForm):
    class Meta:
        model = Marcacao
        fields = ['nome', 'apelido', 'email', 'servicos', 'telefone', 'data', 'descricao', 'estado', 'hora']
