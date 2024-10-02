from django.contrib.auth.models import User
from django.db import models

from Fornecedor.models import Fornecedor

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    imagem = models.ImageField(upload_to='user_image/', default='user_image/img_avatar1.png', null=True, blank=True)

class Produto(models.Model):
    imagem = models.ImageField(upload_to='produtos/')
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    marca = models.ForeignKey('Marca', on_delete=models.CASCADE)
    unidade = models.ForeignKey('Unidade', on_delete=models.CASCADE)
    estoque_minimo = models.IntegerField()
    estoque_maximo = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return f"{self.nome}"

class Categoria(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()

    def __str__(self):
        return f"{self.nome}"

class Marca(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()

    def __str__(self):
        return f"{self.nome}"

class Promocao(models.Model):
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    desconto = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.produto} - Desconto: {self.desconto}%"

class Unidade(models.Model):
    nome = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.nome}"

# class Cliente(models.Model):
#     nome = models.CharField(max_length=255)
#     email = models.EmailField()
#     telefone = models.CharField(max_length=20)
#     endereco = models.CharField(max_length=255)
#     cidade = models.CharField(max_length=255)
#     estado = models.CharField(max_length=2)
#     cep = models.CharField(max_length=8)
    
#     def __str__(self):
#         return f"{self.nome}"

# class Fornecedor(models.Model):
#     nome = models.CharField(max_length=255)
#     email = models.EmailField()
#     telefone = models.CharField(max_length=20)
#     endereco = models.CharField(max_length=255)
#     cidade = models.CharField(max_length=255)
#     estado = models.CharField(max_length=2)
#     cep = models.CharField(max_length=8)

#     class Meta:
#         verbose_name = 'Fornecedor'
#         verbose_name_plural = 'Fornecedores'
    
#     def __str__(self):
#         return f"{self.nome}"

# class Funcionario(models.Model):
#     nome = models.CharField(max_length=255)
#     email = models.EmailField()
#     telefone = models.CharField(max_length=20)
#     endereco = models.CharField(max_length=255)
#     cidade = models.CharField(max_length=255)
#     estado = models.CharField(max_length=2)
#     cep = models.CharField(max_length=8)
    
#     class Meta:
#         verbose_name = 'Funcionario'
#         verbose_name_plural = 'Funcionarios'
    
#     def __str__(self):
#         return f"{self.nome}"

class Localizacao(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    
    class Meta:
        verbose_name = 'Localização'
        verbose_name_plural = 'Localizações'
    
    def __str__(self):
        return f"{self.nome}"

class OrdemCompra(models.Model):
    fornecedor = models.ForeignKey('Fornecedor.Fornecedor', on_delete=models.CASCADE)
    produtos = models.ManyToManyField('Produto', through='ItemOrdemCompra')
    data_emissao = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Ordem de Compra'
        verbose_name_plural = 'Ordens de Compra'
    
    def __str__(self):
        return f"{self.fornecedor}"+" - "+f"{self.data_emissao}"+" - R$"+f"{self.total}"


class ItemOrdemCompra(models.Model):
    ordem_compra = models.ForeignKey('OrdemCompra', on_delete=models.CASCADE, null=False, blank=False)
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE, null=False, blank=False)
    quantidade = models.IntegerField(null=False, blank=False)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)

    class Meta:
        verbose_name = 'Item Ordem de Compra'
        verbose_name_plural = 'Itens Ordem de Compra'
    
    def __str__(self):
        return f"{self.produto}"

class OrdemVenda(models.Model):
    cliente = models.ForeignKey('Cliente.Cliente', on_delete=models.CASCADE)
    produtos = models.ManyToManyField('Produto', through='ItemOrdemVenda')
    data_emissao = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Ordem de Venda'
        verbose_name_plural = 'Ordens de Venda'
    
    def __str__(self):
        return f"{self.cliente}"+" - "+f"{self.data_emissao}"

class ItemOrdemVenda(models.Model):
    ordem_venda = models.ForeignKey('OrdemVenda', on_delete=models.CASCADE)
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Item Ordem de Venda'
        verbose_name_plural = 'Itens Ordem de Venda'
    
    def __str__(self):
        return f"{self.produto}"

class ConfiguracaoSistema(models.Model):
    informacoes_contato = models.TextField(verbose_name='Informação de contato', help_text='Informação de contato')
    termos_de_uso = models.TextField(verbose_name='Termo de uso', help_text='Termo de uso')
    politicas_privacidade = models.TextField(verbose_name='Politica privacidade', help_text='Politica privacidade')

    class Meta:
        verbose_name = 'Configuração de Sistema'
        verbose_name_plural = 'Configurações de Sistema'
    
    def __str__(self):
        return f"{self.informacoes_contato}"