from django.contrib import admin

from Cliente.models import Cliente

# Register your models here.

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'email','endereco', 'cidade', 'estado', 'cep',)
    search_fields = ('nome', 'telefone', 'email','endereco', 'cidade', 'estado', 'cep',)

admin.site.register(Cliente,ClienteAdmin)