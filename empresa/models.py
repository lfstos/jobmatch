from django.db import models
from choices.choices import get_faixa_salarial_choices, get_escolaridade_choices

class Empresa(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class Vaga(models.Model):
    nome_vaga = models.CharField(max_length=100)
    faixa_salarial = models.CharField(max_length=5, choices=get_faixa_salarial_choices)
    escolaridade = models.CharField(max_length=18, choices=get_escolaridade_choices)
    requisitos = models.TextField()
    empresa = models.ForeignKey(Empresa, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nome_vaga
