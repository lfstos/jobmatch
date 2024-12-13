from django.shortcuts import render
from usuarios.forms import UsuarioForm

def home(request):
    if request.method == 'GET':
        form = UsuarioForm()
    return render(request, 'usuarios/home.html', {'form': form})