from django.http import HttpResponse
from django.shortcuts import render
from vagas.forms import VagaForm, CandidatoForm
from vagas.models import Vaga, Candidato
from usuarios.models import User


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
    vagas = Vaga.objects.all()
    return render(request, 'vagas/lista_vagas.html', {'vagas': vagas})


def candidatar_vaga(request):
    if request.method == 'POST':
        form = CandidatoForm(request.POST)
        if form.is_valid():
            candidato = Candidato(
                email=User.objects.get(id=request.POST.get('email')),
                faixa_salarial=request.POST.get('faixa_salarial'),
                escolaridade=request.POST.get('escolaridade'),
                experiencia=request.POST.get('experiencia'),
            )
            candidato.save()
            vaga = Vaga.objects.get(id=request.POST.get('vaga'))
            candidato.vagas.set([vaga])
            candidato.save()
            return render(request, 'vagas/candidatar_vaga.html')
        return HttpResponse('Falha ao cadandidatar')
