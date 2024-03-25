from django.contrib import admin
from .models import *






class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'preco',)
    search_fields = ('nome', 'descricao', 'preco',)

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao',)
    search_fields = ('nome', 'descricao',)

class PromocaoAdmin(admin.ModelAdmin):
    list_display = ('produto', 'Categoria','data_inicio','data_fim','desconto','status',)
    search_fields = ('produto', 'Categoria','data_inicio','data_fim','desconto','status',)

class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao',)
    search_fields = ('nome', 'descricao',)

class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'email',)
    search_fields = ('nome', 'telefone', 'email',)

class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'email',)
    search_fields = ('nome', 'email', 'email',)

class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'endereco', 'cidade', 'estado', 'cep',)
    search_fields = ('nome', 'email', 'telefone', 'endereco', 'cidade', 'estado', 'cep',)

class LocalizacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao',)
    search_fields = ('nome', 'descricao',)


admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Promocao, PromocaoAdmin)
admin.site.register(Marca, MarcaAdmin)
admin.site.register(Unidade, UnidadeAdmin)
admin.site.register(Cliente,ClienteAdmin)
admin.site.register(Fornecedor,FornecedorAdmin)
admin.site.register(Funcionario, FuncionarioAdmin)
admin.site.register(Localizacao, LocalizacaoAdmin)

class ItemOrdemCompraInline(admin.TabularInline):
    model = ItemOrdemCompra
    extra = 1

class OrdemCompraAdmin(admin.ModelAdmin):
    inlines = (ItemOrdemCompraInline,)

class ItemOrdemVendaInline(admin.TabularInline):
    model = ItemOrdemVenda
    extra = 1

class OrdemVendaAdmin(admin.ModelAdmin):
    inlines = (ItemOrdemVendaInline,)

admin.site.register(OrdemCompra, OrdemCompraAdmin)
admin.site.register(OrdemVenda, OrdemVendaAdmin)
admin.site.register(ConfiguracaoSistema)