from django import forms
from choices.choices import get_faixa_salarial_choices, get_escolaridade_choices
from .models import User
from vagas.models import Vaga

class VagaForm(forms.Form):
    nome_vaga = forms.CharField(max_length=100)
    faixa_salarial = forms.ChoiceField(choices=get_faixa_salarial_choices)
    escolaridade = forms.ChoiceField(choices=get_escolaridade_choices)
    requisitos = forms.CharField(widget=forms.Textarea)
    empresa = forms.ModelChoiceField(queryset=User.objects.none()) # inicializa com queryset vazio

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(VagaForm, self).__init__(*args, **kwargs)
        if user:
            # Filtra a empresa do usuário logado
            self.fields['empresa'].queryset = User.objects.filter(email=user.email)


# class CandidatoForm(forms.Form):
#     email = forms.ModelChoiceField(queryset=User.objects.none())  # inicializa com queryset vazio
#     faixa_salarial = forms.ChoiceField(choices=get_faixa_salarial_choices)
#     escolaridade = forms.ChoiceField(choices=get_escolaridade_choices)
#     experiencia = forms.CharField(widget=forms.Textarea)
#     vaga = forms.ModelChoiceField(queryset=Vaga.objects.none())  # inicializa com queryset vazio

#     def __init__(self, *args, **kwargs):
#         super(CandidatoForm, self).__init__(*args, **kwargs)
#         self.fields['email'].queryset = User.objects.filter(is_company=False)
#         self.fields['vaga'].queryset = Vaga.objects.all()



class CandidatoForm(forms.Form):
    email = forms.ModelChoiceField(queryset=User.objects.none()) # inicializa com queryset vazio
    faixa_salarial = forms.ChoiceField(choices=get_faixa_salarial_choices)
    escolaridade = forms.ChoiceField(choices=get_escolaridade_choices)
    experiencia = forms.CharField(widget=forms.Textarea)
    vaga = forms.ModelChoiceField(queryset=Vaga.objects.none()) # inicializa com queryset vazio

    def __init__(self, *args, **kwargs):
        super(CandidatoForm, self).__init__(*args, **kwargs)
        self.fields['email'].queryset = User.objects.filter(is_company=False)
        self.fields['vaga'].queryset = Vaga.objects.all()