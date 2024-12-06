from django.db import models
from choices.choices import get_faixa_salarial_choices, get_escolaridade_choices
from vagas.models import Vaga
from usuarios.models import User


class Candidato(models.Model):
    email = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # nome = models.CharField(max_length=100)
    faixa_salarial = models.CharField(max_length=5, choices=get_faixa_salarial_choices)
    escolaridade = models.CharField(max_length=18, choices=get_escolaridade_choices)
    experiencia = models.TextField()
    vagas = models.ManyToManyField(Vaga)
