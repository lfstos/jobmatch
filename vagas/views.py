from django.http import HttpResponse
from django.shortcuts import render
from vagas.forms import VagaForm, CandidatoForm
from vagas.models import Vaga, Candidato
from usuarios.models import User


def cadastrar_vagas(request):
    if request.method == 'POST':
        if request.POST.get('is_company') == 'True':
            form = VagaForm(request.POST)
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
        else:
            raise Exception('Apenas Empresa pode cadastrar vagas!')
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
            id = form.cleaned_data['email'].id # Obtendo o ID do usuário
            candidato = Candidato.objects.create(
                email=User.objects.get(id=id),
                faixa_salarial=form.cleaned_data['faixa_salarial'],
                escolaridade=form.cleaned_data['escolaridade'],
                experiencia=form.cleaned_data['experiencia'],
            )
            vaga_id = request.POST.get('vaga') # obtendo o ID da vaga
            vaga = Vaga.objects.get(id=vaga_id) # usando diretamente o ID da vaga
            candidato.vagas.set([vaga])
            candidato.save()
            return render(request, 'vagas/candidatar_vaga.html')
        return HttpResponse('Falha ao cadandidatar')


def editar_vaga(request):
    if request.method == 'POST':
        if request.POST.get('is_company'):
            # Recupera o id da empresa que deseja alterar
            id = request.POST.get('vaga')
            vaga = Vaga.objects.get(id=id)
            form = VagaForm(request.POST)
            if form.is_valid():
                vaga.nome_vaga=form.cleaned_data['nome_vaga']
                vaga.faixa_salarial=form.cleaned_data['faixa_salarial']
                vaga.escolaridade=form.cleaned_data['escolaridade']
                vaga.requisitos=form.cleaned_data['requisitos']
                vaga.empresa=form.cleaned_data['empresa']
                vaga.save()
                return render(request, 'vagas/lista_vagas.html')
        else:
            return HttpResponse('não é empresa')
        

def excluir_vaga(request):
    if request.method == 'POST':
        if request.POST.get('is_company') == 'True':
            id = request.POST.get('vaga')
            vaga = Vaga.objects.filter(id=id)
            vaga.delete()
            return render(request, 'vagas/lista_vagas.html')
        else:
            raise Exception('Apenas empresa pode excluir vaga!')
        
    