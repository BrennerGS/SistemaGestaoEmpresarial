from django import forms
from .models import Produto, Cliente, Fornecedor, Funcionario, Categoria, Marca, Unidade, Localizacao #, OrdemCompra, OrdemVenda, RelatorioVendas, RelatorioEstoque, RelatorioFornecedores, Usuario, Permissao, Configuracao, IntegracaoApi, IntegracaoComercioEletronico, IntegracaoPagamento, IntegracaoEnvio, IntegracaoMarketing, IntegracaoCrm, IntegracaoIntegraçãoDados
from .models import *
from django.forms import inlineformset_factory

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'categoria', 'marca', 'unidade', 'estoque_minimo', 'estoque_maximo', 'preco', 'imagem','descricao']

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'telefone', 'endereco', 'cidade', 'estado', 'cep']

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['nome', 'email', 'telefone', 'endereco', 'cidade', 'estado', 'cep']

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'email', 'telefone', 'endereco', 'cidade', 'estado', 'cep']

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao']

class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nome', 'descricao']

class UnidadeForm(forms.ModelForm):
    class Meta:
        model = Unidade
        fields = ['nome']

class LocalizacaoForm(forms.ModelForm):
    class Meta:
        model = Localizacao
        fields = ['nome', 'descricao']


class OrdemCompraForm(forms.ModelForm):
    class Meta:
        model = OrdemCompra
        fields = ['fornecedor', 'total']

ItemOrdemCompraFormSet = inlineformset_factory(OrdemCompra, ItemOrdemCompra, fields=('produto', 'quantidade', 'preco_unitario'), extra=2, can_delete=True)

class ItemOrdemCompraForm(forms.ModelForm):
    class Meta:
        model = ItemOrdemCompra
        fields = ['quantidade', 'preco_unitario']

class OrdemVendaForm(forms.ModelForm):
    class Meta:
        model = OrdemVenda
        fields = ['cliente', 'total']

ItemOrdemVendaFormSet = inlineformset_factory(OrdemVenda, ItemOrdemVenda, fields=('produto', 'quantidade', 'preco_unitario'), extra=2, can_delete=True)

class ItemOrdemVendaForm(forms.ModelForm):
    class Meta:
        model = ItemOrdemVenda
        fields = ['quantidade', 'preco_unitario']

class ConfiguracaoSistemaForm(forms.ModelForm):
    class Meta:
        model = ConfiguracaoSistema
        fields = ['informacoes_contato', 'termos_de_uso', 'politicas_privacidade']
        

# ----------------------------------------------------------------------------
# class OrdemCompraForm(forms.ModelForm):
#     class Meta:
#         model = OrdemCompra
#         fields = ['fornecedor', 'produto', 'quantidade', 'preco', 'data_entrega']

# class OrdemVendaForm(forms.ModelForm):
#     class Meta:
#         model = OrdemVenda
#         fields = ['cliente', 'produto', 'quantidade', 'preco', 'data_entrega']

# class RelatorioVendasForm(forms.ModelForm):
#     class Meta:
#         model = RelatorioVendas
#         fields = ['periodo', 'produto', 'cliente', 'valor_total', 'quantidade']

# class RelatorioEstoqueForm(forms.ModelForm):
#     class Meta:
#         model = RelatorioEstoque
#         fields = ['produto', 'estoque_atual', 'estoque_minimo', 'estoque_maximo']

# class RelatorioFornecedoresForm(forms.ModelForm):
#     class Meta:
#         model = RelatorioFornecedores
#         fields = ['periodo', 'fornecedor', 'produto', 'valor_total']

# class UsuarioForm(forms.ModelForm):
#     class Meta:
#         model = Usuario
#         fields = ['nome', 'email', 'telefone', 'endereco', 'cidade', 'estado', 'cep', 'permissoes']

# class PermissaoForm(forms.ModelForm):
#     class Meta:
#         model = Permissao
#         fields = ['nome']

# class ConfiguracaoForm(forms.ModelForm):
#     class Meta:
#         model = Configuracao
#         fields = ['informacoes_contato', 'termos_uso', 'politicas_privacidade']

# class IntegracaoApiForm(forms.ModelForm):
#     class Meta:
#         model = IntegracaoApi
#         fields = ['nome', 'informacoes_integracao']

# class IntegracaoComercioEletronicoForm(forms.ModelForm):
#     class Meta:
#         model = IntegracaoComercioEletronico
#         fields = ['plataforma', 'informacoes_integracao']

# class IntegracaoPagamentoForm(forms.ModelForm):
#     class Meta:
#         model = IntegracaoPagamento
#         fields = ['plataforma', 'informacoes_integracao']

# class IntegracaoEnvioForm(forms.ModelForm):
#     class Meta:
#         model = IntegracaoEnvio
#         fields = ['plataforma', 'informacoes_integracao']

# class IntegracaoMarketingForm(forms.ModelForm):
#     class Meta:
#         model = IntegracaoMarketing
#         fields = ['plataforma', 'informacoes_integracao']

# class IntegracaoCrmForm(forms.ModelForm):
#     class Meta:
#         model = IntegracaoCrm
#         fields = ['plataforma', 'informacoes_integracao']

# class IntegracaoIntegraçãoDadosForm(forms.ModelForm):
#     class Meta:
#         model = IntegracaoIntegraçãoDados
#         fields = ['plataforma', 'informacoes_integracao']
