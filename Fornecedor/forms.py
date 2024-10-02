from django import forms
from .models import Fornecedor
from .models import *
from django.forms import inlineformset_factory


class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['nome', 'email', 'telefone', 'endereco', 'cidade', 'estado', 'cep']
