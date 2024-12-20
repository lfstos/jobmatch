from django import forms
from django.contrib.auth.forms import UserCreationForm
from usuarios.models import User


class UsuarioForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), label=''
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}), label=''

    )
    


class CadastroForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), label=''
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}), label=''
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar Senha'}), label=''

    )
    is_company = forms.ChoiceField(
        choices=[('False', 'Não'), ('True', 'Sim')],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=''
    )

    class Meta:
        model = User
        fields=['email', 'password1', 'password2', 'is_company']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save
        return user
