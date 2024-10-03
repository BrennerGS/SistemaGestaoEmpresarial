from django import forms
from .models import ConfiguracaoSistema
from django.forms import inlineformset_factory


class ConfiguracaoForm(forms.ModelForm):
    class Meta:
        model = ConfiguracaoSistema
        fields = ['informacoes_contato', 'termos_de_uso', 'politicas_privacidade']
