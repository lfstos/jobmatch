from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate

from usuarios.forms import UsuarioForm, CadastroForm
from usuarios.models import User


def index(request):
    if request.method == 'GET':
        form = UsuarioForm()
        return render(request, 'usuarios/home.html', {'form': form})


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            return redirect('listar_vagas')
        else:
            messages.error(request, 'Usuário ou senha inválidos')
            form = UsuarioForm()
            return render(request, 'usuarios/home.html', {'form': form, 'alert': 'alert-danger'})


def cadastro(request):
    if request.method == 'GET':
        return render(request, 'usuarios/cadastro.html', {'form': CadastroForm()})
    elif request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
                is_company=form.cleaned_data['is_company']
            )
            messages.success(request, 'Usuário cadastrado com sucesso')
            return render(request, 'usuarios/home.html', {'form': UsuarioForm(), 'alert': 'alert-success'})
        else:
            messages.error(request, form.errors)
            return render(request, 'usuarios/cadastro.html', {'form': form})