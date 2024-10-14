from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from core.usuario.forms import LoginForm
from core.usuario.forms import CandidatoRegistrationForm


def register_candidato(request):
    if request.method == 'POST':
        form = CandidatoRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_company = False  # Define o usuário como candidato
            user.save()
            return redirect('login')
    else:
        form = CandidatoRegistrationForm()
    return render(request, 'users/register_candidato.html', {'form': form})


def register_empresa(request):
    if request.method == 'POST':
        form = CandidatoRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_company = True  # Define o usuário como empresa
            user.save()
            return redirect('login')
    else:
        form = CandidatoRegistrationForm()
    return render(request, 'users/register_empresa.html', {'form': form})


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'
