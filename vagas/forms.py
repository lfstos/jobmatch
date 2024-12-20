from django import forms
from choices.choices import get_faixa_salarial_choices, get_escolaridade_choices
from .models import User
from vagas.models import Vaga

class VagaForm(forms.Form):
    nome_vaga = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da vaga'}), label='')
  
    faixa_salarial = forms.ChoiceField(
        choices=[('', 'Selecione pretensão salarial')] + list(get_faixa_salarial_choices()),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    escolaridade = forms.ChoiceField(
        choices=[('', 'Selecione a escolaridade')] + list(get_escolaridade_choices()), widget=forms.Select(
            attrs={
                'class': 'form-select',
                'placeholder': 'Selecione'
            })
    )
    requisitos = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição da vaga'}), label='')
    empresa = forms.ModelChoiceField(queryset=User.objects.none(),
                                     widget=forms.TextInput(attrs={'class': 'form-select'})
    ) # inicializa com queryset vazio

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['empresa'].queryset = User.objects.filter(is_company=True)
        # self.fields['faixa_salarial'].widget.attrs['class']='form-select'


class CandidatoForm(forms.Form):
    email = forms.ModelChoiceField(queryset=User.objects.none()) # inicializa com queryset vazio
    faixa_salarial = forms.ChoiceField(
        choices=[('', 'Selecione a pretensão salarial')] + list(get_faixa_salarial_choices()), widget=forms.Select(
            attrs={'class': 'form-select'}
        )
    )
    escolaridade = forms.ChoiceField(
        choices=[('', 'Selecione a escolaridade')] + list(get_escolaridade_choices()), widget=forms.Select(
            attrs={'class': 'form-select'}
        )
    )
    experiencia = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Qual sua experiência?'})
    )
    vaga = forms.ModelChoiceField(queryset=Vaga.objects.none()) # inicializa com queryset vazio

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].queryset = User.objects.filter(is_company=False)
        self.fields['vaga'].queryset = Vaga.objects.all()