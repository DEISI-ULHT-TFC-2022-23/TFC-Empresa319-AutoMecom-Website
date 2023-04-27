from django.db import models


# Create your models here.

class Servico(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=250, default="", blank=True)

    def __str__(self):
        return self.nome[:40]
