from django.shortcuts import render, redirect
from usuarios.forms import UsuarioForm, CadastroForm
from django.contrib import messages
from django.http import HttpResponse
from usuarios.models import User


def home(request):
    if request.method == 'GET':
        form = UsuarioForm()
        return render(request, 'usuarios/home.html', {'form': form})
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        return HttpResponse('Acessar o sistema...')


def cadastro(request):
    form = CadastroForm()
    if request.method == 'GET':
        return render(request, 'usuarios/cadastro.html', {'form': form})
    elif request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
                is_company=form.cleaned_data['is_company']
            )
            messages.success(request, 'Usuário cadastrado com sucesso')
            # return render(request, 'usuarios/home.html', {'form': UsuarioForm()})
            return redirect('home')
        else:
            print(form.errors)
            messages.error(request, form.errors)
            return render(request, 'usuarios/cadastro.html', {'form': form})