from django import forms
from .models import Cliente
from .models import *
from django.forms import inlineformset_factory


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'telefone', 'endereco', 'cidade', 'estado', 'cep']
