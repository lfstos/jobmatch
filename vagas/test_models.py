import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from empresa.models import Empresa
from usuarios.models import User
from vagas.models import Vaga, Candidato

User = get_user_model()


@pytest.mark.django_db
def test_cadastra_um_candidato_para_uma_vaga():
    user = User.objects.create_user(
        email='candidato@candidato.com', password='candidato'
    )
    empresa = Empresa.objects.create(email='email@email.com')
    vaga = Vaga.objects.create(nome_vaga='Desenvolvedor Python/Django', empresa=empresa)

    candidato = Candidato.objects.create(
        email = user,
        faixa_salarial = '1k-2k',
        escolaridade = 'Tecnologo',
        experiencia = 'Experiência com 5 anos em Python/Django.',
    )

    candidato.vagas.set([vaga])
    assert candidato.email.email == 'candidato@candidato.com'
    assert candidato.faixa_salarial == '1k-2k'
    assert candidato.escolaridade == 'Tecnologo'
    assert candidato.experiencia == 'Experiência com 5 anos em Python/Django.'
    assert vaga in candidato.vagas.all()


@pytest.mark.django_db
def test_cadastra_um_candidato_para_duas_vagas():
    user = User.objects.create_user(
        email='candidato@candidato.com', password='candidato'
    )
    empresa = Empresa.objects.create(email='empresa@empresa.com')
    vaga1 = Vaga.objects.create(
        nome_vaga='DBA',
        empresa=empresa,
        faixa_salarial='3k+',
        requisitos='Experiência com DBA e Oracle',
        escolaridade='Doutorado'
    )
    vaga2 = Vaga.objects.create(
        nome_vaga='Frontend',
        empresa=empresa,
        faixa_salarial='1k-2k',
        requisitos='Experiência com Javascript',
        escolaridade='Tecnologo'
    )

    candidato = Candidato.objects.create(
        email=user,
        faixa_salarial='3k+',
        escolaridade='Doutorado',
        experiencia='Experiênte com DBA usando Oracle.',
    )
    candidato.vagas.set([vaga1, vaga2])
    assert candidato.email.email == 'candidato@candidato.com'
    assert candidato.faixa_salarial == '3k+'
    assert candidato.escolaridade == 'Doutorado'
    assert candidato.experiencia == 'Experiênte com DBA usando Oracle.'
    assert vaga1 in candidato.vagas.all()
    assert vaga2 in candidato.vagas.all()

    # Verifica IDs
    vagas_ids = candidato.vagas.values_list('id', flat=True)
    assert vaga1.id in vagas_ids
    assert vaga2.id in vagas_ids


@pytest.mark.django_db
def test_cria_uma_vaga():
    client = Client()

    # Criação de uma empresa e um usuário para associar à vaga
    user = User.objects.create_user(email='empresa@empresa.com', password='testpassword')
    empresa = Empresa(email='empresa@empresa.com')
    empresa.save()

    # Autentica o usuário
    client.login(email='empresa@empresa.com', password='testpassword')

    # Dados do formulário
    dados_formulario= {
        'nome_vaga': 'Desenvolvedor Python',
        'faixa_salarial': '3k+',
        'escolaridade': 'Doutorado',
        'requisitos': 'Python, Django, Banco de Dados NoSQL e SQL',
        'empresa': empresa.id # Se o form precisar do ID da empresa
    }

    # Faz a requisição POST para a view
    url = reverse('cadastrar_vagas')
    response = client.post(url, dados_formulario)

    # Exibe a resposta para ver detalhes dos erros, se houver
    if response.status_code != 200:
        print(response.content.decode())  # Adiciona essa linha para imprimir detalhes dos erros
    assert response.status_code == 200  # ou 302 se houver redirecionamento

    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200

    # Verifica se a vaga foi criada
    vaga = Vaga.objects.get(nome_vaga='Desenvolvedor Python')
    assert vaga.nome_vaga == 'Desenvolvedor Python'
    assert vaga.faixa_salarial == '3k+'
    assert vaga.escolaridade == 'Doutorado'
    assert vaga.requisitos == 'Python, Django, Banco de Dados NoSQL e SQL'
    assert vaga.empresa.email == empresa.email


@pytest.mark.django_db
def test_candidata_uma_vaga():
    client = Client()

    user = User.objects.create_user(email='candidato@candidato.com', password='candidato')
