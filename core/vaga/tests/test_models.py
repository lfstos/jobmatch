import pytest
from core.vaga.models import Vaga, Candidatura
from django.contrib.auth import get_user_model


User = get_user_model()

"""
Testes Vagas e Cadidaturas
"""


@pytest.mark.django_db
def test_criar_vaga():
    user = User.objects.create_user(email='empresa@example.com', password='password', is_company=True)
    vaga = Vaga.objects.create(
        nome='Desenvolvedor Python',
        faixa_salarial='2000-3000',
        requisitos='Experiência com Django',
        escolaridade_minima='SUPERIOR',
        empresa=user
    )
    assert vaga.nome == 'Desenvolvedor Python'
    assert vaga.empresa == user


@pytest.mark.django_db
def test_candidatar_vaga():
    empresa = User.objects.create_user(email='empresa@example.com', password='password', is_company=True)
    candidato = User.objects.create_user(email='candidato@example.com', password='password', is_company=False)
    vaga = Vaga.objects.create(
        nome='Desenvolvedor Python',
        faixa_salarial='2000-3000',
        requisitos='Experiência com Django',
        escolaridade_minima='SUPERIOR',
        empresa=empresa
    )
    candidatura = Candidatura.objects.create(
        candidato=candidato,
        vaga=vaga,
        pretensao_salarial='2000-3000',
        experiencia='2 anos',
        ultima_escolaridade='SUPERIOR'
    )
    assert candidatura.candidato == candidato
    assert candidatura.vaga == vaga
