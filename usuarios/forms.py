from django import forms


class UsuarioForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(), label='Senha', )