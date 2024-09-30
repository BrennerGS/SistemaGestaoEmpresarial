from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     
     path('', dashboard, name='dashboard'),

     path('produtos/', produto_list, name='lista_produtos'),
     path('produto/create', produto_create, name='produto_create'),
     path('produto/edit/<int:pk>', produto_edit, name='produto_edit'),
     path('produto/delete/<int:pk>', produto_delete, name='produto_delete'),
     
     path('categorias/', Categoria_list, name='Categoria_list'),
     path('categoria/create', Categoria_create, name='Categoria_create'),
     path('categoria/edit/<int:pk>', Categoria_edit, name='Categoria_edit'),
     path('categoria/delete/<int:pk>', Categoria_delete, name='Categoria_delete'),

     path('promocao/', Promocao_list, name='Promocao_list'),
     path('promocao/create', Promocao_create, name='Promocao_create'),
     path('promocao/edit/<int:pk>', Promocao_edit, name='Promocao_edit'),
     path('promocao/delete/<int:pk>', Promocao_delete, name='Promocao_delete'),

     path('unidades/', Unidade_list, name='Unidade_list'),
     path('unidade/create', Unidade_create, name='Unidade_create'),
     path('unidade/edit/<int:pk>', Unidade_edit, name='Unidade_edit'),
     path('unidade/delete/<int:pk>', Unidade_delete, name='Unidade_delete'),

     path('Marca_list/', Marca_list, name='Marca_list'),
     path('Marca/create', Marca_create, name='Marca_create'),
     path('Marca/edit/<int:pk>', Marca_edit, name='Marca_edit'),
     path('Marca/delete/<int:pk>', Marca_delete, name='Marca_delete'),

     path('Fornecedor/', Fornecedor_list, name='Fornecedor_list'),
     path('Fornecedor/create', Fornecedor_create, name='Fornecedor_create'),
     path('Fornecedor/edit/<int:pk>', Fornecedor_edit, name='Fornecedor_edit'),
     path('Fornecedor/delete/<int:pk>', Fornecedor_delete, name='Fornecedor_delete'),

     path('Funcionario/', Funcionario_list, name='Funcionario_list'),
     path('Funcionario/create', Funcionario_create, name='Funcionario_create'),
     path('Funcionario/edit/<int:pk>', Funcionario_edit, name='Funcionario_edit'),
     path('Funcionario/delete/<int:pk>', Funcionario_delete, name='Funcionario_delete'),

     path('Localizacao/', Localizacao_list, name='Localizacao_list'),
     path('Localizacao/create', Localizacao_create, name='Localizacao_create'),
     path('Localizacao/edit/<int:pk>', Localizacao_edit, name='Localizacao_edit'),
     path('Localizacao/delete/<int:pk>', Localizacao_delete, name='Localizacao_delete'),

     path('ordem_compra/', ordem_compra_list, name='ordem_compra_list'),
     path('ordem_compra/adicionar/', adicionar_ordem_compra, name='adicionar_ordem_compra'),
     path('ordem_compra/adicionar/<int:extra>/', adicionar_ordem_compra, name='adicionar_ordem_compraExtra'),
     path('ordem_compra/editar/<int:pk>/', editar_ordem_compra, name='editar_ordem_compra'),
     path('ordem_compra/editar/extra/<int:pk>/<int:extra>/', editar_ordem_compra, name='editar_ordem_compraExtra'),
     path('ordem_compra/item/deletar/<int:pk>/', deletar_itemordem_compra, name='deletar_itemordem_compra'),
     path('ordem_compra/deletar/<int:pk>/', deletar_ordem_compra, name='deletar_ordem_compra'),

     path('ordem_venda/', ordem_venda_list, name='ordem_venda_list'),
     path('ordem_venda/adicionar/', adicionar_ordem_venda, name='adicionar_ordem_venda'),
     path('ordem_venda/adicionar/<int:extra>/', adicionar_ordem_venda, name='adicionar_ordem_vendaExtra'),
     path('ordem_venda/editar/<int:pk>/', editar_ordem_venda, name='editar_ordem_venda'),
     path('ordem_venda/editar/extra/<int:pk>/<int:extra>/', editar_ordem_venda, name='editar_ordem_vendaExtra'),
     path('ordem_venda/item/deletar/<int:pk>/', deletar_itemordem_venda, name='deletar_itemordem_venda'),
     path('ordem_venda/deletar/<int:pk>/', deletar_ordem_venda, name='deletar_ordem_venda'),

     path('configuracao_sistema/', configuracao_sistema_list, name='configuracao_sistema_list'),
     path('configuracao_sistema/adicionar/', adicionar_configuracao_sistema, name='adicionar_configuracao_sistema'),
     path('configuracao_sistema/editar/<int:pk>/', editar_configuracao_sistema, name='editar_configuracao_sistema'),
     path('configuracao_sistema/deletar/<int:pk>/', deletar_configuracao_sistema, name='deletar_configuracao_sistema'),

     # path('api_request/', api_request_view, name='api_request'),
]