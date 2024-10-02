from django import forms
from .models import Funcionario
from .models import *
from django.forms import inlineformset_factory


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'email', 'telefone', 'endereco', 'cidade', 'estado', 'cep']
