
from django.contrib.auth.models import User
from django.db import models


class TipoServico(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Servico(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=350, default="", blank=True)
    tipo = models.ManyToManyField(TipoServico)

    def __str__(self):
        return self.nome


class Veiculo(models.Model):
    marca = models.CharField(max_length=200)
    modelo = models.CharField(max_length=200)
    ano = models.PositiveIntegerField(default=0000)
    matricula = models.CharField(max_length=8)
    kms = models.IntegerField(default=0)

    def __str__(self):
        return self.marca + " " + self.modelo


class Utilizador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    administrador = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Marcacao(models.Model):
    utilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE, related_name="marcacoes", blank=True,
                                   null=True)
    nome = models.CharField(max_length=200)
    apelido = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    telefone = models.IntegerField()
    servicos = models.ManyToManyField(Servico)
    veiculo = models.OneToOneField(Veiculo, on_delete=models.CASCADE)
    data = models.CharField(max_length=200, default=0)
    hora = models.CharField(max_length=200, default=0)
    descricao = models.TextField(max_length=500)

    ESTADOS = [
        ('PC', 'Por confirmar'),
        ('CO', "Confirmado"),
        ('Fi', 'Terminado')
    ]
    estado = models.CharField(max_length=50, choices=ESTADOS, default='PC')

    numero = models.IntegerField(default=0)
    orcamento = models.TextField(max_length=500, default="a definir")
    observacoes = models.TextField(max_length=500, default=" ")
    fatura = models.FileField(upload_to='tarefas/', null=True, blank=True)

    def __str__(self):
        return f"{self.nome} - {self.data}"
