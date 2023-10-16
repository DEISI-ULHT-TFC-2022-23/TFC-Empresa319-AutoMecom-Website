from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

from .models import Servico, Utilizador, Veiculo, Marcacao, TipoServico
from .widget import DatePickerInput, TimePickerInput


class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['tipo', 'nome', 'descricao']


class TipoServicoForm(forms.ModelForm):
    class Meta:
        model = TipoServico
        fields = ['nome']


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Nome próprio'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Apelido'
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
        self.fields['password1'].widget.attrs['placeholder'] = 'Palavra passe'
        self.fields['password2'].widget.attrs['placeholder'] = '********'

        self.fields['username'].help_text = '150 caracteres ou menos. Somente letras, dígitos e @/./+/-/_.'
        self.fields['password1'].help_text = 'Sua senha deve conter pelo menos 8 caracteres.'
        self.fields['password2'].help_text = 'Digite a mesma senha de antes, para verificação.'


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = '150 caracteres ou menos. Somente letras, dígitos e @/./+/-/_.'


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

        self.fields['new_password1'].help_text = ''


class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['marca', 'modelo', 'ano', 'matricula', 'kms']


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
        fields = ['nome', 'apelido', 'email', 'servicos', 'telefone', 'data', 'descricao', 'estado', 'hora',
                  'orcamento', 'observacoes', 'fatura']


class MarcacaoEditFormClient(forms.ModelForm):
    class Meta:
        model = Marcacao
        fields = ['nome', 'apelido', 'email', 'servicos', 'telefone', 'data', 'descricao', 'hora']
