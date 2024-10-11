from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from core.vaga.models import Vaga, Candidatura
from django.db.models import Count
from datetime import datetime
from core.vaga.forms import VagaForm


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


@login_required(login_url='login')
def criar_vaga(request):
    if request.method == 'POST':
        form = VagaForm(request.POST)
        if form.is_valid():
            vaga = form.save(commit=False)
            vaga.empresa = request.user
            vaga.save()
            return redirect('lista_vagas')
    else:
        form = VagaForm()
    return render(request, 'vagas/criar_vaga.html', {'form': form})


def detalhe_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    return render(request, 'vagas/detalhe_vaga.html', {'vaga': vaga})


@login_required(login_url='login')
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
