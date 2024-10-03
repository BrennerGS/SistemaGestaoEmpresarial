from django.db import models

# Create your models here.
class ConfiguracaoSistema(models.Model):
    informacoes_contato = models.TextField(verbose_name='Informação de contato', help_text='Informação de contato')
    termos_de_uso = models.TextField(verbose_name='Termo de uso', help_text='Termo de uso')
    politicas_privacidade = models.TextField(verbose_name='Politica privacidade', help_text='Politica privacidade')

    class Meta:
        verbose_name = 'Configuração de Sistema'
        verbose_name_plural = 'Configurações de Sistema'
    
    def __str__(self):
        return f"{self.informacoes_contato}"