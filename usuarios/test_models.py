import pytest
from django.test import Client
from django.urls import reverse
from .models import User

@pytest.mark.django_db
def test_cria_candidato():
    
    client = Client()

    payload = {
        'email': 'candidato@candidato',
        'password1': 'testpassword',
        'password2': 'testpassword',
    }
    url = reverse('cadastro')
    response = client.post(url, payload)

    assert response.status_code == 200
    

@pytest.mark.django_db
def test_cria_empresa():
    empresa = User.objects.create_user(email="empresa@empresa.com", password="empresa", is_company=True)
    assert empresa.email == "empresa@empresa.com"
    assert empresa.is_company


@pytest.mark.django_db
def test_normalisa_email():
    usuario = User.objects.create_user(email="AdMin@aDmIn.com", password="AdMin@aDmIn", is_company=False)
    assert usuario.email == "admin@admin.com"
    assert not usuario.is_company


@pytest.mark.django_db
def test_cria_usuario_sem_senha():
    with pytest.raises(ValueError, match="The given password must be set"):
        usuario = User.objects.create_user(email="usuario@usuario.com", password="", is_company=False)
        assert usuario.email == "usuario@usuario.com"


@pytest.mark.django_db
def test_cria_usuario_sem_email():
    with pytest.raises(ValueError, match="The given email must be set"):
        usuario = User.objects.create_user(email="", password="usuario", is_company=False)
        assert usuario.email == "usuario@usuario.com"


def test_home():
    client = Client()
    response = client.get('/')
    assert response.status_code == 200
    # assert 'home' in response.home.html


# @pytest.mark.django_db
# def test_criar_usuario():
    
    
#     client = Client()
