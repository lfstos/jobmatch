from django.db import models
from core.usuario.models import CustomUser


class Vaga(models.Model):
    SALARIO_OPCOES = [
        ('ATÉ 1.000', 'Até 1.000'),
        ('DE 1.000 A 2.000', 'De 1.000 a 2.000'),
        ('DE 2.000 A 3.000', 'De 2.000 a 3.000'),
        ('ACIMA DE 3.000', 'Acima de 3.000'),
    ]

    ESCOLARIDADE_OPCOES = [
        ('FUNDAMENTAL', 'Ensino fundamental'),
        ('MEDIO', 'Ensino médio'),
        ('TECNOLOGO', 'Tecnólogo'),
        ('SUPERIOR', 'Ensino Superior'),
        ('POS', 'Pós / MBA / Mestrado'),
        ('DOUTORADO', 'Doutorado'),
    ]

    empresa = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_company': True})
    nome = models.CharField(max_length=255)
    faixa_salarial = models.CharField(max_length=16, choices=SALARIO_OPCOES)
    requisitos = models.TextField()
    escolaridade_minima = models.CharField(max_length=11, choices=ESCOLARIDADE_OPCOES)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.nome


class Candidatura(models.Model):
    candidato = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_company': False})
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE, related_name='candidaturas')
    data_candidatura = models.DateTimeField(auto_now_add=True)
    pretensao_salarial = models.CharField(max_length=16, choices=Vaga.SALARIO_OPCOES)
    experiencia = models.TextField()
    ultima_escolaridade = models.CharField(max_length=11, choices=Vaga.ESCOLARIDADE_OPCOES)

    def _str_(self):
        return f'{self.candidato.email} -> {self.vaga.nome}'
