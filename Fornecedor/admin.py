from django.contrib import admin

from Fornecedor.models import Fornecedor

# Register your models here.

class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'email',)
    search_fields = ('nome', 'email', 'email',)

admin.site.register(Fornecedor,FornecedorAdmin)