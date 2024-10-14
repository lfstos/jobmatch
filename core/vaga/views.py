import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from core.vaga.models import Vaga, Candidatura
from django.db.models import Count
from datetime import datetime
from core.vaga.forms import VagaForm, CandidaturaForm


def lista_vagas(request):
    vagas = Vaga.objects.all()
    return render(request, 'vagas/lista_vagas.html', {'vagas': vagas})


@login_required(login_url='login')
def relatorio(request):
    vagas_por_mes = Vaga.objects.filter(data_criacao__year=datetime.now().year).values('data_criacao__month').annotate(
        total=Count('id'))
    candidatos_por_mes = Candidatura.objects.filter(data_candidatura__year=datetime.now().year).values(
        'data_candidatura__month').annotate(total=Count('id'))

    # Garantir que os meses e dados sejam convertidos corretamente para strings
    meses_vagas = [str(v['data_criacao__month']) for v in vagas_por_mes]
    total_vagas = [v['total'] for v in vagas_por_mes]
    meses_candidatos = [str(c['data_candidatura__month']) for c in candidatos_por_mes]
    total_candidatos = [c['total'] for c in candidatos_por_mes]

    return render(request, 'vagas/relatorio.html', {
        'meses': meses_vagas,
        'vagas': total_vagas,
        'meses_candidatos': meses_candidatos,
        'candidatos': total_candidatos,
    })


logger = logging.getLogger(__name__)


@login_required(login_url='login')
def criar_vaga(request):
    if request.method == 'POST':
        form = VagaForm(request.POST)
        if form.is_valid():
            vaga = form.save(commit=False)
            vaga.empresa = request.user
            vaga.save()
            logger.info("Vaga criada com sucesso. Redirecionando para 'lista_vagas'.")
            return redirect('lista_vagas')
        else:
            logger.warning("Formulário inválido. Erros: %s", form.errors)
    else:
        form = VagaForm()
    return render(request, 'vagas/criar_vaga.html', {'form': form})

# def detalhe_vaga(request, vaga_id):
#     vaga = get_object_or_404(Vaga, id=vaga_id)
#     return render(request, 'vagas/detalhe_vaga.html', {'vaga': vaga})


# @login_required(login_url='login')
@login_required(login_url='login')
def detalhe_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    candidaturas = vaga.candidaturas.all()  # Usando o related_name 'candidaturas'

    # Pontuando candidatos
    def pontuar_candidato(candidatura):
        pontos = 0

        # Pontuação por faixa salarial
        if candidatura.pretensao_salarial == vaga.faixa_salarial:
            pontos += 1

        # Lista de escolaridades em ordem crescente de importância
        ordem_escolaridade = [
            'FUNDAMENTAL', 'MEDIO', 'TECNOLOGO', 'SUPERIOR', 'POS', 'DOUTORADO'
        ]

        # Pontuação por escolaridade
        if ordem_escolaridade.index(candidatura.ultima_escolaridade) >= ordem_escolaridade.index(vaga.escolaridade_minima):
            pontos += 1

        return pontos

    # Calcula os pontos para cada candidatura
    for candidatura in candidaturas:
        candidatura.pontos = pontuar_candidato(candidatura)
        logger.info(f'Candidatura: {candidatura}, Pontos: {candidatura.pontos}')

    return render(request, 'vagas/detalhe_vaga.html', {'vaga': vaga, 'candidaturas': candidaturas})


def editar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    if request.method == 'POST':
        form = VagaForm(request.POST, instance=vaga)
        if form.is_valid():
            form.save()
            return redirect('detalhe_vaga', vaga_id=vaga.id)
    else:
        form = VagaForm(instance=vaga)
    return render(request, 'vagas/editar_vaga.html', {'form': form})


def deletar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    if request.method == 'POST':
        vaga.delete()
        return redirect('lista_vagas')
    return render(request, 'vagas/deletar_vaga.html', {'vaga': vaga})


@login_required
def candidatar_vaga(request, vaga_id):
    vaga = Vaga.objects.get(id=vaga_id)
    if request.method == 'POST':
        form = CandidaturaForm(request.POST)
        if form.is_valid():
            candidatura = form.save(commit=False)
            candidatura.candidato = request.user
            candidatura.vaga = vaga
            candidatura.save()
            return redirect('detalhe_vaga', vaga_id=vaga.id)
    else:
        form = CandidaturaForm()
    return render(request, 'vagas/candidatar_vaga.html', {'form': form, 'vaga': vaga})
