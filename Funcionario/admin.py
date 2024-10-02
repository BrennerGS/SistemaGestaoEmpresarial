from django.contrib import admin

from Funcionario.models import Funcionario

# Register your models here.

class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone','endereco', 'cidade', 'estado', 'cep',)
    search_fields = ('nome', 'email', 'telefone','endereco', 'cidade', 'estado', 'cep',)

admin.site.register(Funcionario,FuncionarioAdmin)