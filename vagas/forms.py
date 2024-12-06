from django import forms
from choices.choices import get_faixa_salarial_choices, get_escolaridade_choices
from empresa.models import Empresa

class VagaForm(forms.Form):
    nome_vaga = forms.CharField(max_length=100)
    faixa_salarial = forms.ChoiceField(choices=get_faixa_salarial_choices)
    escolaridade = forms.ChoiceField(choices=get_escolaridade_choices)
    requisitos = forms.CharField(widget=forms.Textarea)
    empresa = forms.ModelChoiceField(queryset=Empresa.objects.none()) # inicializa com queryset vazio

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(VagaForm, self).__init__(*args, **kwargs)
        if user:
            # Filtra a empresa do usuário logado
            self.fields['empresa'].queryset = Empresa.objects.filter(email=user.email)
