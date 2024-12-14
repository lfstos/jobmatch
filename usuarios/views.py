from django.shortcuts import render
from usuarios.forms import UsuarioForm
from django.http import HttpResponse

def home(request):
    if request.method == 'GET':
        form = UsuarioForm()
        return render(request, 'usuarios/home.html', {'form': form})
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        return HttpResponse(f'{email} - {password}')
