from django.contrib import admin

from configuracao.models import ConfiguracaoSistema

# Register your models here.

class ConfiguracaoSistemaAdmin(admin.ModelAdmin):
    list_display = ('informacoes_contato', 'termos_de_uso', 'politicas_privacidade')
    search_fields = ('informacoes_contato', 'termos_de_uso', 'politicas_privacidade')

admin.site.register(ConfiguracaoSistema,ConfiguracaoSistemaAdmin)