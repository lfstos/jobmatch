from datetime import datetime

import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.vaga.models import Vaga, Candidatura

User = get_user_model()

"""
Teste as views para criar vagas, candidatar-se a vagas e verificar pontuações.
"""


@pytest.mark.django_db
def test_criar_vaga_view(client):
    User.objects.create_user(email='admin@admin.com', password='admin', is_company=True)
    client.login(email='admin@admin.com', password='admin')
    response = client.post(reverse('criar_vaga'), {
        'nome': 'Desenvolvedor Python',
        'faixa_salarial': 'DE 2.000 A 3.000',
        'requisitos': 'Experiência com Django',
        'escolaridade_minima': 'SUPERIOR'
    })
    assert response.status_code == 302
    assert Vaga.objects.filter(nome='Desenvolvedor Python').exists()
    print(response.content.decode())


@pytest.mark.django_db
def test_candidatar_vaga_view(client):
    empresa = User.objects.create_user(email='empresa@example.com', password='password', is_company=True)
    candidato = User.objects.create_user(email='candidato@example.com', password='password', is_company=False)
    vaga = Vaga.objects.create(
        nome='Desenvolvedor Python',
        faixa_salarial='DE 2.000 A 3.000',
        requisitos='Experiência com Django',
        escolaridade_minima='SUPERIOR',
        empresa=empresa
    )
    client.login(email='candidato@example.com', password='password')
    response = client.post(reverse('candidatar_vaga', args=[vaga.id]), {
        'pretensao_salarial': 'DE 2.000 A 3.000',
        'experiencia': '2 anos',
        'ultima_escolaridade': 'SUPERIOR'
    })
    assert response.status_code == 302
    assert Candidatura.objects.filter(candidato=candidato, vaga=vaga).exists()


@pytest.mark.django_db
def test_relatorio_view(client):
    empresa = User.objects.create_user(email='admin@admin.com', password='admin', is_company=True)
    client.login(email='admin@admin.com', password='admin')

    # Criação de vagas e candidaturas para testar o relatório
    for i in range(1, 4):
        Vaga.objects.create(
            nome=f'Vaga {i}',
            faixa_salarial='2000-3000',
            requisitos='Experiência com Django',
            escolaridade_minima='SUPERIOR',
            empresa=empresa,
            data_criacao=datetime(year=2024, month=i, day=1)
        )

    response = client.get(reverse('relatorio'))
    assert response.status_code == 200
    assert 'Vagas Criadas' in response.content.decode()
    assert 'Candidatos Recebidos' in response.content.decode()


@pytest.mark.django_db
def test_detalhe_vaga_view_pontuacao(client):
    empresa = User.objects.create_user(email='empresa@empresa.com', password='password', is_company=True)
    candidato = User.objects.create_user(email='candidato@candidato.com', password='password', is_company=False)
    vaga = Vaga.objects.create(
        nome='Desenvolvedor Python',
        faixa_salarial='2000-3000',
        requisitos='Experiência com Django',
        escolaridade_minima='SUPERIOR',
        empresa=empresa
    )
    Candidatura.objects.create(
        candidato=candidato,
        vaga=vaga,
        pretensao_salarial='2000-3000',
        experiencia='2 anos',
        ultima_escolaridade='SUPERIOR'
    )
    client.login(email='empresa@empresa.com', password='password')
    response = client.get(reverse('detalhe_vaga', args=[vaga.id]))
    assert response.status_code == 200
    print(response.content.decode())
    assert 'Pontos: 2' in response.content.decode()
