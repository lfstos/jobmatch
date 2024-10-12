from django import forms
from core.vaga.models import Vaga, Candidatura


class VagaForm(forms.ModelForm):
    nome = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}), label='')
    faixa_salarial = forms.ChoiceField(
        choices=Vaga.SALARIO_OPCOES,
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )
    requisitos = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Requisitos'}), label='')
    escolaridade_minima = forms.ChoiceField(
        choices=Vaga.ESCOLARIDADE_OPCOES,
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )

    class Meta:
        model = Vaga
        fields = ['nome', 'faixa_salarial', 'requisitos', 'escolaridade_minima']


class CandidaturaForm(forms.ModelForm):
    class Meta:
        model = Candidatura
        fields = ['pretensao_salarial', 'experiencia', 'ultima_escolaridade']
