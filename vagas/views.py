from django.http import HttpResponse
from django.shortcuts import render
from vagas.forms import VagaForm
from vagas.models import Vaga

def cadastrar_vagas(request):
    if request.method == 'POST':
        form = VagaForm(request.POST, user=request.user)
        if form.is_valid():
            vaga = Vaga.objects.create(
                nome_vaga=form.cleaned_data['nome_vaga'],
                faixa_salarial=form.cleaned_data['faixa_salarial'],
                escolaridade=form.cleaned_data['escolaridade'],
                requisitos=form.cleaned_data['requisitos'],
                empresa=form.cleaned_data['empresa'],
            )
            vaga.save()
            return HttpResponse('Vaga cadastrada com sucesso')
        else:
            return HttpResponse(f'Formulário inválido: {form.errors.as_json()}', status=400)
    elif request.method == 'GET':
        form = VagaForm()
        # form = VagaForm(user=request.user)
        return render(request, 'vagas/cadastrar_vagas.html', {'form': form})


def lista_vagas(request):
    # TODO: Escrever teste para essa view
    vagas = Vaga.objects.all()
    return render(request, 'vagas/lista_vagas.html', {'vagas': vagas})
    