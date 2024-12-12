import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from usuarios.models import User
from vagas.models import Vaga, Candidato

User = get_user_model()


@pytest.mark.django_db
def test_cadastra_um_candidato_para_uma_vaga():
    user = User.objects.create_user(
        email='candidato@candidato.com', password='candidato', is_company=False
    )
    empresa = User.objects.create_user(email='empresa@empresa.com', password='empresa', is_company=True)
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
        email='candidato@candidato.com', password='candidato', is_company=False
    )
    empresa = User.objects.create(email='empresa@empresa.com', password='empresa', is_company=True)
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
def test_criar_uma_vaga():
    
    client = Client()

    # Criação de uma empresa e um usuário para associar à vaga
    # user = User.objects.create_user(email='empresa@empresa.com', password='testpassword')
    empresa = User.objects.create_user(email='empresa@empresa.com', password='testpassword', is_company=True)

    # Autentica o usuário
    client.login(email='empresa@empresa.com', password='testpassword')

    # Dados do formulário
    payload= {
        'nome_vaga': 'Desenvolvedor Python',
        'faixa_salarial': '3k+',
        'escolaridade': 'Doutorado',
        'requisitos': 'Python, Django, Banco de Dados NoSQL e SQL',
        'empresa': empresa.id, # Se o form precisar do ID da empresa
        'is_company': empresa.is_company,
    }

    # Faz a requisição POST para a view
    url = reverse('cadastrar_vagas')
    response = client.post(url, payload)

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


# @pytest.mark.django_db
# def test_candidata_uma_vaga():
#     client = Client()

#     user = User.objects.create_user(email='candidato@candidato.com', password='testpassword')


@pytest.mark.django_db
def test_lista_com_uma_vaga():
    
    client = Client()

    # Criação de uma empresa para criar uma vaga
    empresa = User.objects.create(email='empresa@empresa.com', password='testpassword', is_company=True)
    
    # Criação da vaga com a instância Empresa
    Vaga.objects.create(
        nome_vaga='Desenvolvedor Django',
        faixa_salarial='3k+',
        escolaridade='Doutorado',
        requisitos='Saber desenvolvimento web',
        empresa=empresa
    )

    # Fazendo uma requisição GET à view lista_vagas
    response = client.get(reverse('lista_vagas'))
    
    # Verificando se o status da resposta é 200 (OK)
    assert response.status_code == 200

    # Verificando se a vaga criada está no contexto da resposta
    assert 'vagas' in response.context
    assert response.context['vagas'].count() == 1
    assert response.context['vagas'].first().nome_vaga == 'Desenvolvedor Django'

@pytest.mark.django_db
def test_lista_com_cinco_vagas():
    
    client = Client()

    # Criação de uma empresa para criar cinco vagas
    empresa = User.objects.create(email='empresa@empresa.com', password='testpassword', is_company=True)

    # Criação das vagas com a instância da Empresa
    Vaga.objects.create(nome_vaga = 'Desenvolvedor Django', empresa=empresa)
    Vaga.objects.create(nome_vaga = 'Desenvolvedor Python', empresa=empresa)
    Vaga.objects.create(nome_vaga = 'Analista de Dados', empresa=empresa)
    Vaga.objects.create(nome_vaga = 'Gerente de Projetos', empresa=empresa)
    Vaga.objects.create(nome_vaga = 'Engenheiro de Software', empresa=empresa)

    # Fazendo a reauisição GET à view lista_vagas
    response = client.get(reverse('lista_vagas'))

    # Verificando se o status da resposta é 200 (OK)
    assert response.status_code == 200
    
    # Verficando se todas as 5 vagas criadas estão no contexto da resposta
    assert response.context['vagas'].count() == 5

    # Verificação adicioan para garantir que os nomes das vagas estão corretas
    nomes_vagas = [vaga.nome_vaga for vaga in response.context['vagas']]
    assert 'Desenvolvedor Django' in nomes_vagas
    assert 'Desenvolvedor Python' in nomes_vagas
    assert 'Analista de Dados' in nomes_vagas
    assert 'Gerente de Projetos' in nomes_vagas
    assert 'Engenheiro de Software' in nomes_vagas


@pytest.mark.django_db
def test_candidatar_vaga():

    client = Client()

    # Criando um Usuário que irá representar o candidato
    usuario = User.objects.create_user(email='usuario@usuario.com', password='usuario', is_company=False)

    # Criando uma instância de Empresa
    empresa = User.objects.create_user(email='empresa@empresa.com', password='empresa', is_company=True)

    # Criando uma instância de Vaga
    vaga = Vaga.objects.create(
        nome_vaga='Desenvolvedor Django',
        faixa_salarial='1k-2k',
        escolaridade='Ensino Medio',
        requisitos='Proeficiente em API Rest',
        empresa=empresa
    )

    # Criação da Candidatura
    payload = {
        'email': usuario.id,
        'faixa_salarial': '1k-2k',
        'escolaridade': 'Tecnologo',
        'experiencia': 'Sou desenvolvedor web com especialidade Django',
        'vaga': vaga.id
    }

    url = reverse('candidatar_vaga')
    response = client.post(url, payload)
    assert response.status_code == 200

    # candidato = Candidato.objects.get(email=usuario.email)
    candidato = Candidato.objects.get(email=usuario)
    # assert vaga.faixa_salarial == '1k-2k'
    # assert vaga.escolaridade == 'Tecnologo'
    # assert vaga.experiencia == 'Sou desenvolvedor web com especialidade Django'
    # assert vaga.vagas.filter(id=vaga.id).exists()


@pytest.mark.django_db
def test_editar_vaga():
    
    client = Client()

    empresa = User.objects.create_user(email='empresa@empresa.com', password='testpassword', is_company=True)

    vaga = Vaga.objects.create(
        nome_vaga='Desenvolvedor Python',
        faixa_salarial='3k+',
        escolaridade='Doutorado',
        requisitos='Conhecer framework Django',
        empresa=empresa
    )

    assert vaga.nome_vaga == 'Desenvolvedor Python'
    assert vaga.faixa_salarial == '3k+'
    assert vaga.escolaridade == 'Doutorado'
    assert vaga.requisitos == 'Conhecer framework Django'
    assert vaga.empresa == empresa
    
    payload = {
        'nome_vaga':'Desenvolvedor NodeJS',
        'faixa_salarial': '1k-2k',
        'escolaridade': 'Tecnologo',
        'requisitos': 'Conhecer Javascript',
        'vaga': vaga.id,
        'is_company': empresa.is_company,
        'empresa': empresa.id
    }

    url = reverse('editar_vaga')
    response = client.post(url, payload)

    assert response.status_code == 200

    vaga = Vaga.objects.get(id=vaga.id)

    assert vaga.nome_vaga == 'Desenvolvedor NodeJS'
    assert vaga.faixa_salarial == '1k-2k'
    assert vaga.escolaridade == 'Tecnologo'
    assert vaga.requisitos == 'Conhecer Javascript'
    assert vaga.id == vaga.id
    assert vaga.empresa == empresa


@pytest.mark.django_db
def test_excluir_vaga_empresa():

    client = Client()

    empresa = User.objects.create_user(email='empresa@empresa.com', password='testpassword', is_company=True)
    vaga = Vaga.objects.create(nome_vaga='Desenvolvedor Web', empresa=empresa)

    assert vaga.nome_vaga == 'Desenvolvedor Web'
    assert vaga.empresa == empresa

    payload={
        'vaga': vaga.id,
        'usuario': empresa.id,
        'is_company': empresa.is_company
    }

    assert vaga.nome_vaga == 'Desenvolvedor Web'
    assert empresa == empresa

    url = reverse('excluir_vaga')
    response = client.post(url, payload)

    assert response.status_code == 200

    vaga = Vaga.objects.all()

    assert vaga.count() == 0


@pytest.mark.django_db
def test_excluir_vaga_candidato_gera_excessao():

    client = Client()

    candidato = User.objects.create_user(email='candidato@candidato.com', password='testpassword', is_company=False)
    vaga = Vaga.objects.create(
        nome_vaga='Estágio de desenvolvimento Backend',
        faixa_salarial='1k',
        escolaridade='Ensino Fundamental',
        requisitos='Proeficiencia em Python',
        empresa=candidato,
    )
    assert vaga.nome_vaga == 'Estágio de desenvolvimento Backend'
    assert vaga.faixa_salarial == '1k'
    assert vaga.escolaridade == 'Ensino Fundamental'
    assert vaga.requisitos == 'Proeficiencia em Python'

    payload = {'vaga': vaga.id, 'is_company': candidato.is_company}
    url = reverse('excluir_vaga')

    with pytest.raises(Exception, match='Apenas empresa pode excluir vaga!'):
        client.post(url, payload)
        


@pytest.mark.django_db
def test_criar_vaga_candidato_gera_excessao():

    client = Client()

    candidato = User.objects.create_user(email='candidato@candidato.com', password='testpassword', is_company=False)
    vaga = Vaga.objects.create(
        nome_vaga='Desenvolvedor Web',
        faixa_salarial='1k-2k',
        escolaridade='Tecnologo',
        requisitos='Framework Django',
        empresa=candidato
    )

    payload = {
        'nome_vaga': vaga.nome_vaga,
        'faixa_salarial': '',
        'escolaridade': '',
        'requisitos': '',
        'empresa': candidato.id,
        'is_company': candidato.is_company
    }
    
    url = reverse('cadastrar_vagas')

    with pytest.raises(Exception, match='Apenas Empresa pode cadastrar vagas!'):
        response = client.post(url, payload)
    