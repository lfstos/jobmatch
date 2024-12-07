from django.db import models

from empresa.models import Empresa
from choices.choices import get_escolaridade_choices, get_faixa_salarial_choices
from usuarios.models import User


class Vaga(models.Model):
    nome_vaga = models.CharField(max_length=100)
    faixa_salarial = models.CharField(max_length=5, choices=get_faixa_salarial_choices)
    escolaridade = models.CharField(max_length=18, choices=get_escolaridade_choices)
    requisitos = models.TextField()
    empresa = models.ForeignKey(Empresa, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.nome_vaga


class Candidato(models.Model):
    email = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    faixa_salarial = models.CharField(max_length=5, choices=get_faixa_salarial_choices)
    escolaridade = models.CharField(max_length=18, choices=get_escolaridade_choices)
    experiencia = models.TextField()
    vagas = models.ManyToManyField(Vaga)
