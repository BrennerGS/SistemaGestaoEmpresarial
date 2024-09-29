import logging
import logging.config
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import *
from django.forms import formset_factory
from .models import *
from .utils import *
from .fields import *
from django.core.paginator import Paginator
from django.core.cache import cache
from django.contrib.auth.decorators import  login_required, permission_required

Qtd = 20




def set_list_value_in_cache(list):
    # Verifica se o valor 'list' está na URL e o define no cache
    list_value = list
    if list_value:
        cache.set('list_value', list_value, timeout=300)  # O timeout é em segundos

def get_list_value_from_cache():
    # Obtém o valor de 'list' do cache, se não estiver disponível, usa um valor padrão
    return cache.get('list_value', '20')


def api_request_GET(request):
    # Exemplo de URL e parâmetros (ajuste conforme necessário)
    api_url = 'https://jsonplaceholder.typicode.com/posts'
    api_method = 'GET'
    api_headers = {'Authorization': 'Bearer SEU_TOKEN'}
    api_params = {'parametro1': 'valor1', 'parametro2': 'valor2'}

    # Faz a requisição à API usando a função genérica
    response = make_api_request(api_url, method=api_method, headers=api_headers, params=api_params)

    # Renderiza um template com a resposta da API
    return render(request, 'api_response.html', {'api_response': response})

def api_request_POST(request):
    # Exemplo de URL e parâmetros (ajuste conforme necessário)
    api_url = 'https://jsonplaceholder.typicode.com/posts'
    api_method = 'POST'
    api_headers = {'Authorization': 'Bearer SEU_TOKEN'}
    api_params = {'parametro1': 'valor1', 'parametro2': 'valor2'}

    # Faz a requisição à API usando a função genérica
    response = make_api_request(api_url, method=api_method, headers=api_headers, params=api_params)

    # Renderiza um template com a resposta da API
    return render(request, 'api_response.html', {'api_response': response})

def api_request_PUT(request):
    # Exemplo de URL e parâmetros (ajuste conforme necessário)
    api_url = 'https://jsonplaceholder.typicode.com/posts'
    api_method = 'PUT'
    api_headers = {'Authorization': 'Bearer SEU_TOKEN'}
    api_params = {'parametro1': 'valor1', 'parametro2': 'valor2'}

    # Faz a requisição à API usando a função genérica
    response = make_api_request(api_url, method=api_method, headers=api_headers, params=api_params)

    # Renderiza um template com a resposta da API
    return render(request, 'api_response.html', {'api_response': response})

def api_request_PATCH(request):
    # Exemplo de URL e parâmetros (ajuste conforme necessário)
    api_url = 'https://jsonplaceholder.typicode.com/posts'
    api_method = 'PATCH'
    api_headers = {'Authorization': 'Bearer SEU_TOKEN'}
    api_params = {'parametro1': 'valor1', 'parametro2': 'valor2'}

    # Faz a requisição à API usando a função genérica
    response = make_api_request(api_url, method=api_method, headers=api_headers, params=api_params)

    # Renderiza um template com a resposta da API
    return render(request, 'api_response.html', {'api_response': response})

def api_request_DELETE(request):
    # Exemplo de URL e parâmetros (ajuste conforme necessário)
    api_url = 'https://jsonplaceholder.typicode.com/posts'
    api_method = 'DELETE'
    api_headers = {'Authorization': 'Bearer SEU_TOKEN'}
    api_params = {'parametro1': 'valor1', 'parametro2': 'valor2'}

    # Faz a requisição à API usando a função genérica
    response = make_api_request(api_url, method=api_method, headers=api_headers, params=api_params)

    # Renderiza um template com a resposta da API
    return render(request, 'api_response.html', {'api_response': response})


def dashboard(request):
    
    return render(request, 'dashboard.html')

@login_required
@permission_required('produtos.view_produto',raise_exception=True)
def produto_list(request):
    
    if request.GET.get("list") and request.GET.get("list").isdigit():
        set_list_value_in_cache(int(request.GET.get("list")))
        Qtlist = 20

        return redirect('lista_produtos')
    
    else:
        Qtlist = get_list_value_from_cache()
    
    user_profiles = UserProfile.objects.filter(user=request.user)

    # Verifique se o queryset está vazio
    if user_profiles.exists():
        UserProfiles = user_profiles.first()
    else:
        UserProfiles = None 

    model_list = Produto.objects.all()
    paginator = Paginator(model_list, Qtlist) 

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'UserProfiles': UserProfiles,
        'model_name': 'Produtos',
        'object_list': page_obj,
        'ActionAdd': ListAction(url_name='produto_create', label='Adicionar Produto', icon='fa fa-plus', cor='w3-green'),
        'list_actions': [
            ListAction(url_name='produto_edit', label='Atualizar', icon='fa fa-edit', cor='w3-blue'),
            ListAction(url_name='produto_delete', label='Excluir', icon='fa fa-trash', cor='w3-red'),
        ],
        'column_titles' : [f.name for f in Produto._meta.fields],
        'get_attribute': get_attribute,
    }
    return render(request, 'generico/base_list.html', context)

@login_required
@permission_required('produtos.add_produto',raise_exception=True)
def produto_create(request):
        if request.method == 'POST' :
            try:    
                form = ProdutoForm(request.POST, request.FILES)
                if form.is_valid():
                    try:
                        form.save()
                        messages.success(request, "Atualização realizada com sucesso!")
                        return redirect('lista_produtos')
                            
                    except Exception as e:
                        messages.warning(request, "Erro ao validar dados, por favor preencha corretamente ou tente novamente mais tarde!")
                        return redirect('lista_produtos')
            except Exception as e:
                messages.warning(request, "Erro por favor tente novamente mais tarde!")
                return redirect('lista_produtos')
        else:
            form = ProdutoForm()
        context = {
            'fieldName' : [
                #ListAction(id=1,formGen = FormCategoria, url_name='Categoria_create', name='categoria', label='Inserir', icon='fa fa-edit', cor='w3-blue'),    
                ListAction(id=2,url_name='Categoria_list', name='categoria', label='Visualizar', icon='fa fa-edit', cor='w3-blue'),
                #ListAction(id=3,formGen = FormMarca, url_name='Marca_create', name='marca', label='Inserir', icon='fa fa-edit', cor='w3-blue'),    
                ListAction(id=4,url_name='Marca_list', name='marca', label='Visualizar', icon='fa fa-edit', cor='w3-blue'),
                #ListAction(id=5,formGen = FormUnidade, url_name='Unidade_create', name='unidade', label='Inserir', icon='fa fa-edit', cor='w3-blue'),    
                ListAction(id=6,url_name='Unidade_list', name='unidade', label='Visualizar', icon='fa fa-edit', cor='w3-blue'),
            ],
        }

        return render(request, 'generico/form.html', {'form': form, 'a': context, 'model_name':'Cadastro de Produto', 'ActionCancel': 'lista_produtos'})


@login_required
@permission_required('produtos.change_produto')
def produto_edit(request, pk):
        produto = get_object_or_404(Produto, pk=pk)
        if request.method == 'POST':
            try:
                form = ProdutoForm(request.POST, request.FILES, instance=produto)
                if form.is_valid():
                    try:
                        form.save()
                        messages.success(request, "Atualização realizada com sucesso!")

                        return redirect('lista_produtos')
                                
                    except Exception as e:
                        messages.warning(request, "Erro ao validar dados, por favor preencha corretamente ou tente novamente mais tarde!")
                        return redirect('lista_produtos')
            except Exception as e:
                messages.warning(request, "Erro por favor tente novamente mais tarde!")
            return redirect('lista_produtos')
        else:
            form = ProdutoForm(instance=produto)

        context = {
            'fieldName' : [
                #ListAction(id=1,formGen = FormCategoria, url_name='Categoria_create', name='categoria', label='Inserir', icon='fa fa-edit', cor='w3-blue'),    
                ListAction(id=2,url_name='Categoria_list', name='categoria', label='Visualizar', icon='fa fa-search', cor='w3-blue'),
                #ListAction(id=3,formGen = FormMarca, url_name='Marca_create', name='marca', label='Inserir', icon='fa fa-edit', cor='w3-blue'),    
                ListAction(id=4,url_name='Marca_list', name='marca', label='visualizar', icon='fa fa-search', cor='w3-blue'),
                #ListAction(id=5,formGen = FormUnidade, url_name='Unidade_create', name='unidade', label='Inserir', icon='fa fa-edit', cor='w3-blue'),    
                ListAction(id=6,url_name='Unidade_list', name='unidade', label='visualizar', icon='fa fa-search', cor='w3-blue'),
            ],
        }

        return render(request, 'generico/form.html', {'form': form, 'a': context, 'model_name':'Atualizar Produto', 'ActionCancel': 'lista_produtos'})

@login_required
@permission_required('produtos.delete_produto')
def produto_delete(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        return redirect('lista_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'generico/form_delete.html', {'form': form,'delete': produto, 'model_name':'Deletar Produto', 'ActionCancel': 'lista_produtos'})


@login_required
@permission_required('produtos.view_categoria')
def Categoria_list(request):

    if request.GET.get("list"):
        set_list_value_in_cache(int(request.GET.get("list")))

        return redirect('Categoria_list')
    
    else:
        Qtlist = get_list_value_from_cache()

    model_list = Categoria.objects.all()
    paginator = Paginator(model_list, Qtlist) 

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'model_name': 'Categoria',
        'object_list': page_obj,
        'ActionAdd': ListAction(url_name='Categoria_create', label='Adicionar Categoria', icon='fa fa-plus', cor='w3-green'),
        'list_actions': [
            ListAction(url_name='Categoria_edit', label='Atualizar', icon='fa fa-edit', cor='w3-blue'),
            ListAction(url_name='Categoria_delete', label='Excluir', icon='fa fa-trash', cor='w3-red'),
        ],
        'column_titles' : [f.name for f in Categoria._meta.fields],
        'get_attribute': get_attribute,
    }
    return render(request, 'generico/base_list.html', context)

@login_required
@permission_required('produtos.add_categoria')
def Categoria_create(request):
    if request.method == 'POST':
        try:
            form = CategoriaForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, "Atualização realizada com sucesso!")
                    return redirect('Categoria_list')
                        
                except Exception as e:
                    messages.warning(request, "Erro ao validar dados, por favor preencha corretamente ou tente novamente mais tarde!")
                    return redirect('Categoria_list')
        except Exception as e:
            messages.warning(request, "Erro por favor tente novamente mais tarde!")
            return redirect('Categoria_list')
    else:
        form = CategoriaForm()
    return render(request, 'generico/form.html', {'form': form, 'model_name':'Cadastro de Categoria', 'ActionCancel': 'Categoria_list'})

@login_required
@permission_required('produtos.change_categoria')
def Categoria_edit(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        try:
            form = CategoriaForm(request.POST, request.FILES, instance=categoria)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, "Atualização realizada com sucesso!")

                    return redirect('Categoria_list')
                            
                except Exception as e:
                    messages.warning(request, "Erro ao validar dados, por favor preencha corretamente ou tente novamente mais tarde!")
                    return redirect('Categoria_list')
        except Exception as e:
            messages.warning(request, "Erro por favor tente novamente mais tarde!")
            return redirect('Categoria_list')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'generico/form.html', {'form': form, 'model_name':'Atualizar Categoria', 'ActionCancel': 'Categoria_list'})

@login_required
@permission_required('produtos.delete_categoria')
def Categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('Categoria_list')
    else:
        return render(request, 'generico/form_delete.html', {'delete': categoria, 'model_name':'Deletar Categoria', 'ActionCancel': 'Categoria_list'})

@login_required    
@permission_required('produtos.view_promocao')  
def Promocao_list(request):

    if request.GET.get("list") and request.GET.get("list").isdigit():
        set_list_value_in_cache(int(request.GET.get("list")))
        Qtlist = 20

        return redirect('lista_Promocao')
    
    elif get_list_value_from_cache():
        Qtlist = get_list_value_from_cache()
    
    user_profiles = UserProfile.objects.filter(user=request.user)

    # Verifique se o queryset está vazio
    if user_profiles.exists():
        UserProfiles = user_profiles.first()
    else:
        UserProfiles = None 

    model_list = Promocao.objects.all()
    paginator = Paginator(model_list, Qtlist) 

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'UserProfiles': UserProfiles,
        'model_name': 'Promoções',
        'object_list': page_obj,
        'ActionAdd': ListAction(url_name='Promocao_create', label='Adicionar Promoções', icon='fa fa-plus', cor='w3-green'),
        'list_actions': [
            ListAction(url_name='Promocao_edit', label='Atualizar', icon='fa fa-edit', cor='w3-blue'),
            ListAction(url_name='Promocao_delete', label='Excluir', icon='fa fa-trash', cor='w3-red'),
        ],
        'column_titles' : [f.name for f in Promocao._meta.fields],
        'get_attribute': get_attribute,
    }
    return render(request, 'generico/base_list.html', context)

@login_required    
@permission_required('produtos.add_promocao') 
def Promocao_create(request):
    if request.method == 'POST':
        try:
            form = PromocaoForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, "Atualização realizada com sucesso!")
                    return redirect('Promocao_list')
                        
                except Exception as e:
                    messages.warning(request, "Erro ao validar dados, por favor preencha corretamente ou tente novamente mais tarde!")
                    return redirect('Promocao_list')
        except Exception as e:
            messages.warning(request, "Erro por favor tente novamente mais tarde!")
            return redirect('Promocao_list')
    else:
        form = PromocaoForm()  

        user_profiles = UserProfile.objects.filter(user=request.user)
        
        # Verifique se o queryset está vazio
        if user_profiles.exists():
            UserProfiles = user_profiles.first()
        else:
            UserProfiles = None 
        
        context = {
            'form': form,
            'UserProfiles': UserProfiles,
            'fieldName' : [],
            'model_name':'Cadastro de Promoções',
            'ActionCancel': 'Promocao_list',
        }

        return render(request, 'generico/form.html', context)

@login_required    
@permission_required('produtos.change_promocao') 
def Promocao_edit(request, pk):
    promocao = get_object_or_404(Promocao, pk=pk)
    if request.method == 'POST':
        try:
            form = PromocaoForm(request.POST, request.FILES, instance=promocao)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, "Atualização realizada com sucesso!")

                    return redirect('Promocao_list')
                            
                except Exception as e:
                    messages.warning(request, "Erro ao validar dados, por favor preencha corretamente ou tente novamente mais tarde!")
                    return redirect('Promocao_list')
        except Exception as e:
            messages.warning(request, "Erro por favor tente novamente mais tarde!")
            return redirect('Promocao_list')
    else:
        form = PromocaoForm(instance=promocao)
        
        user_profiles = UserProfile.objects.filter(user=request.user)

        # Verifique se o queryset está vazio
        if user_profiles.exists():
            UserProfiles = user_profiles.first()
        else:
            UserProfiles = None 
        
        context = {
            'form': form,
            'UserProfiles': UserProfiles,
            'fieldName' : [],
            'model_name':'Cadastro de Promoções',
            'ActionCancel': 'Promocao_list',
        }

        return render(request, 'generico/form.html', context)

@login_required    
@permission_required('produtos.delete_promocao') 
def Promocao_delete(request, pk):
    promocao = get_object_or_404(Promocao, pk=pk)
    if request.method == 'POST':
        promocao.delete()
        return redirect('Promocao_list')
    else:   
        form = PromocaoForm(instance=Promocao)

        user_profiles = UserProfile.objects.filter(user=request.user)

        # Verifique se o queryset está vazio
        if user_profiles.exists():
            UserProfiles = user_profiles.first()
        else:
            UserProfiles = None

        context = {
            'form': form,
            'UserProfiles': UserProfiles,
            'delete': promocao,
            'model_name':'Atualizar Promoção',
            'ActionCancel': 'Promocao_list',
            'fieldName' : [],
        }
        
    return render(request, 'generico/form_delete.html', context)

@login_required    
@permission_required('produtos.view_unidade') 
def Unidade_list(request):

    if request.GET.get("list"):
        set_list_value_in_cache(int(request.GET.get("list")))

        return redirect('Unidade_list')
    
    else:
        Qtlist = get_list_value_from_cache()

    model_list = Unidade.objects.all()
    paginator = Paginator(model_list, Qtlist) 

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'model_name': 'Unidade',
        'object_list': page_obj,
        'ActionAdd': ListAction(url_name='Unidade_create', label='Adicionar Unidade', icon='fa fa-plus', cor='w3-green'),
        'list_actions': [
            ListAction(url_name='Unidade_edit', label='Atualizar', icon='fa fa-edit', cor='w3-blue'),
            ListAction(url_name='Unidade_delete', label='Excluir', icon='fa fa-trash', cor='w3-red'),
        ],
        'column_titles' : [f.name for f in Unidade._meta.fields],
        'get_attribute': get_attribute,
    }
    return render(request, 'generico/base_list.html', context)

@login_required    
@permission_required('produtos.add_unidade') 
def Unidade_create(request):
    if request.method == 'POST':
        try:
            form = UnidadeForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, "Atualização realizada com sucesso!")
                    return redirect('Unidade_list')
                        
                except Exception as e:
                    messages.warning(request, "Erro ao validar dados, por favor preencha corretamente ou tente novamente mais tarde!")
                    return redirect('Unidade_list')
        except Exception as e:
            messages.warning(request, "Erro por favor tente novamente mais tarde!")
            return redirect('Unidade_list')
    else:
        form = UnidadeForm()
    return render(request, 'generico/form.html', {'form': form, 'model_name':'Cadastro de Unidade', 'ActionCancel': 'Unidade_list'})

@login_required    
@permission_required('produtos.change_unidade') 
def Unidade_edit(request, pk):
    unidade = get_object_or_404(Unidade, pk=pk)
    if request.method == 'POST':
        try:
            form = UnidadeForm(request.POST, request.FILES, instance=unidade)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, "Atualização realizada com sucesso!")

                    return redirect('Unidade_list')
                            
                except Exception as e:
                    messages.warning(request, "Erro ao validar dados, por favor preencha corretamente ou tente novamente mais tarde!")
                    return redirect('Unidade_list')
        except Exception as e:
            messages.warning(request, "Erro por favor tente novamente mais tarde!")
            return redirect('Unidade_list')
    else:
        form = UnidadeForm(instance=unidade)
    return render(request, 'generico/form.html', {'form': form, 'model_name':'Atualizar Unidade', 'ActionCancel': 'Unidade_list'})

@login_required    
@permission_required('produtos.delete_unidade') 
def Unidade_delete(request, pk):
    unidade = get_object_or_404(Unidade, pk=pk)
    if request.method == 'POST':
        unidade.delete()
        return redirect('Unidade_list')
    else:
        return render(request, 'generico/form_delete.html', {'delete': unidade, 'model_name':'Deletar Unidade', 'ActionCancel': 'Unidade_list'})



@login_required    
@permission_required('produtos.view_marca') 
def Marca_list(request):

    if request.GET.get("list"):
        set_list_value_in_cache(int(request.GET.get("list")))

        return redirect('Marca_list')
    
    else:
        Qtlist = get_list_value_from_cache()

    model_list = Marca.objects.all()
    paginator = Paginator(model_list, Qtlist) 

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'model_name': 'Marca',
        'object_list': page_obj,
        'ActionAdd': ListAction(url_name='Marca_create', label='Adicionar Marca', icon='fa fa-plus', cor='w3-green'),
        'list_actions': [
            ListAction(url_name='Marca_edit', label='Atualizar', icon='fa fa-edit', cor='w3-blue'),
            ListAction(url_name='Marca_delete', label='Excluir', icon='fa fa-trash', cor='w3-red'),
        ],
        'column_titles' : [f.name for f in Marca._meta.fields],
        'get_attribute': get_attribute,
    }
    return render(request, 'generico/base_list.html', context)

@login_required    
@permission_required('produtos.add_marca') 
def Marca_create(request):
    if request.method == 'POST':
        try:
            form = MarcaForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, "Atualização realizada com sucesso!")
                    return redirect('Marca_list')
                        
                except Exception as e:
                    messages.warning(request, "Erro ao validar dados, por favor preencha corretamente ou tente novamente mais tarde!")
                    return redirect('Marca_list')
        except Exception as e:
            messages.warning(request, "Erro por favor tente novamente mais tarde!")
            return redirect('Marca_list')
    else:
        form = MarcaForm()
    return render(request, 'generico/form.html', {'form': form, 'model_name':'Cadastro de Marca', 'ActionCancel': 'Marca_list'})

@login_required    
@permission_required('produtos.change_marca') 
def Marca_edit(request, pk):
    marca = get_object_or_404(Marca, pk=pk)
    if request.method == 'POST':
        try:
            form = MarcaForm(request.POST, request.FILES, instance=marca)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, "Atualização realizada com sucesso!")

                    return redirect('Marca_list')
                            
                except Exception as e:
                    messages.warning(request, "Erro ao validar dados, por favor preencha corretamente ou tente novamente mais tarde!")
                    return redirect('Marca_list')
        except Exception as e:
            messages.warning(request, "Erro por favor tente novamente mais tarde!")
            return redirect('Marca_list')
    else:
        form = MarcaForm(instance=marca)
    return render(request, 'generico/form.html', {'form': form, 'model_name':'Atualizar Marca', 'ActionCancel': 'Marca_list'})

@login_required    
@permission_required('produtos.delete_marca') 
def Marca_delete(request, pk):
    marca = get_object_or_404(Marca, pk=pk)
    if request.method == 'POST':
        marca.delete()
        return redirect('Marca_list')
    else:
        return render(request, 'generico/form_delete.html', {'delete': marca, 'model_name':'Deletar Marca', 'ActionCancel': 'Marca_list'})



@login_required    
@permission_required('produtos.view_cliente') 
def Cliente_list(request):
    
    if request.GET.get("list"):
        set_list_value_in_cache(int(request.GET.get("list")))

        return redirect('lista_produtos')
    
    else:
        Qtlist = get_list_value_from_cache()

    model_list = Cliente.objects.all()
    paginator = Paginator(model_list, Qtlist) 

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'model_name': 'Cliente',
        'object_list': page_obj,
        'ActionAdd': ListAction(url_name='Cliente_create', label='Adicionar Cliente', icon='fa fa-plus', cor='w3-green'),
        'list_actions': [
            ListAction(url_name='Cliente_edit', label='Atualizar', icon='fa fa-edit', cor='w3-blue'),
            ListAction(url_name='Cliente_delete', label='Excluir', icon='fa fa-trash', cor='w3-red'),
        ],
        'column_titles' : [f.name for f in Cliente._meta.fields],
        'get_attribute': get_attribute,
    }
    return render(request, 'generico/base_list.html', context)

@login_required    
@permission_required('produtos.add_cliente') 
def Cliente_create(request):
    if request.method == 'POST':
        try:
            form = ClienteForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, "Atualização realizada com sucesso!")
                    return redirect('Cliente_list')
                        
                except Exception as e:
                    messages.warning(request, "Erro ao validar dados, por favor preencha corretamente ou tente novamente mais tarde!")
                    return redirect('Cliente_list')
        except Exception as e:
            messages.warning(request, "Erro por favor tente novamente mais tarde!")
            return redirect('Cliente_list')
    else:
        form = ClienteForm()
    return render(request, 'generico/form.html', {'form': form, 'model_name':'Cadastro de Cliente', 'ActionCancel': 'Cliente_list'})

@login_required    
@permission_required('produtos.change_cliente') 
def Cliente_edit(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        try:
            form = ClienteForm(request.POST, request.FILES, instance=cliente)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, "Atualização realizada com sucesso!")

                    return redirect('Cliente_list')
                            
                except Exception as e:
                    messages.warning(request, "Erro ao validar dados, por favor preencha corretamente ou tente novamente mais tarde!")
                    return redirect('Cliente_list')
        except Exception as e:
            messages.warning(request, "Erro por favor tente novamente mais tarde!")
            return redirect('Cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'generico/form.html', {'form': form, 'model_name':'Atualizar Cliente', 'ActionCancel': 'Cliente_list'})

@login_required    
@permission_required('produtos.delete_cliente') 
def Cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('Cliente_list')
    else:
        return render(request, 'generico/form_delete.html', {'delete': cliente, 'model_name':'Deletar Cliente', 'ActionCancel': 'Cliente_list'})



@login_required    
@permission_required('produtos.view_fornecedor') 
def Fornecedor_list(request):

    if request.GET.get("list"):
        set_list_value_in_cache(int(request.GET.get("list")))

        return redirect('Fornecedor_list')
    
    else:
        Qtlist = get_list_value_from_cache()

    user_profiles = UserProfile.objects.filter(user=request.user)

    # Verifique se o queryset está vazio
    if user_profiles.exists():
        UserProfiles = user_profiles.first()
    else:
        UserProfiles = None 

    model_list = Fornecedor.objects.all()
    paginator = Paginator(model_list, Qtlist) 

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'UserProfiles': UserProfiles,
        'model_name': 'Fornecedor',
        'object_list': page_obj,
        'ActionAdd': ListAction(url_name='Fornecedor_create', label='Adicionar Fornecedor', icon='fa fa-plus', cor='w3-green'),
        'list_actions': [
            ListAction(url_name='Fornecedor_edit', label='Atualizar', icon='fa fa-edit', cor='w3-blue'),
            ListAction(url_name='Fornecedor_delete', label='Excluir', icon='fa fa-trash', cor='w3-red'),
        ],
        'column_titles' : [f.name for f in Fornecedor._meta.fields],
        'get_attribute': get_attribute,
    }
    return render(request, 'generico/base_list.html', context)

@login_required    
@permission_required('produtos.add_fornecedor') 
def Fornecedor_create(request):
    if request.method == 'POST':
        try:
            form = FornecedorForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    form.save()
            
                    messages.success(request, "Atualização realizada com sucesso!")

                    return redirect('Fornecedor_list')
                        
                except Exception as e:
                    messages.warning(request, "Erro ao validar dados, por favor preencha corretamente ou tente novamente mais tarde!")
                    return redirect('Fornecedor_list')
        except Exception as e:
            messages.warning(request, "Erro por favor tente novamente mais tarde!")
            return redirect('Fornecedor_list')
    else:
        form = FornecedorForm()
    return render(request, 'generico/form.html', {'form': form, 'model_name':'Cadastro de Fornecedor', 'ActionCancel': 'Fornecedor_list'})

@login_required    
@permission_required('produtos.change_fornecedor') 
def Fornecedor_edit(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    if request.method == 'POST':
        try:    
            form = FornecedorForm(request.POST, request.FILES, instance=fornecedor)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, "Atualização realizada com sucesso!")

                    return redirect('Fornecedor_list')
                            
                except Exception as e:
                    messages.warning(request, "Erro ao validar dados, por favor preencha corretamente ou tente novamente mais tarde!")
                    return redirect('Fornecedor_list')
        except Exception as e:
            messages.warning(request, "Erro por favor tente novamente mais tarde!")
            return redirect('Fornecedor_list')
        
    else:
        form = FornecedorForm(instance=fornecedor)
    return render(request, 'generico/form.html', {'form': form, 'model_name':'Atualizar Fornecedor', 'ActionCancel': 'Fornecedor_list'})

@login_required    
@permission_required('produtos.delete_fornecedor') 
def Fornecedor_delete(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    if request.method == 'POST':
        fornecedor.delete()
        return redirect('Fornecedor_list')
    else:
        return render(request, 'generico/form_delete.html', {'delete': fornecedor, 'model_name':'Deletar Fornecedor', 'ActionCancel': 'Fornecedor_list'})



@login_required    
@permission_required('produtos.view_funcionario') 
def Funcionario_list(request):

    if request.GET.get("list"):
        set_list_value_in_cache(int(request.GET.get("list")))

        return redirect('Funcionario_list')
    
    else:
        Qtlist = get_list_value_from_cache()

    model_list = Funcionario.objects.all()
    paginator = Paginator(model_list, Qtlist) 

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'model_name': 'Funcionario',
        'object_list': page_obj,
        'ActionAdd': ListAction(url_name='Funcionario_create', label='Adicionar Funcionario', icon='fa fa-plus', cor='w3-green'),
        'list_actions': [
            ListAction(url_name='Funcionario_edit', label='Atualizar', icon='fa fa-edit', cor='w3-blue'),
            ListAction(url_name='Funcionario_delete', label='Excluir', icon='fa fa-trash', cor='w3-red'),
        ],
        'column_titles' : [f.name for f in Funcionario._meta.fields],
        'get_attribute': get_attribute,
    }
    return render(request, 'generico/base_list.html', context)

@login_required    
@permission_required('produtos.add_funcionario') 
def Funcionario_create(request):
    if request.method == 'POST':
        try:
            form = FuncionarioForm(request.POST, request.FILES)
            
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, "Atualização realizada com sucesso!")

                    return redirect('Funcionario_list')
                        
                except Exception as e:
                    messages.warning(request, "Erro ao validar dados, por favor preencha corretamente ou tente novamente mais tarde!")
                    return redirect('Funcionario_list')
        except Exception as e:
            messages.warning(request, "Erro por favor tente novamente mais tarde!")
            return redirect('Funcionario_list')
    else:
        form = FuncionarioForm()
    return render(request, 'generico/form.html', {'form': form, 'model_name':'Cadastro de Funcionario', 'ActionCancel': 'Funcionario_list'})

@login_required    
@permission_required('produtos.change_funcionario') 
def Funcionario_edit(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == 'POST':
        try:
            form = FuncionarioForm(request.POST, request.FILES, instance=funcionario)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, "Atualização realizada com sucesso!")

                    return redirect('Funcionario_list')
                            
                except Exception as e:
                    messages.warning(request, "Erro ao validar dados, por favor preencha corretamente ou tente novamente mais tarde!")
                    return redirect('Funcionario_list')
        except Exception as e:
            messages.warning(request, "Erro por favor tente novamente mais tarde!")
            return redirect('Funcionario_list')
    else:
        form = FuncionarioForm(instance=funcionario)
    return render(request, 'generico/form.html', {'form': form, 'model_name':'Atualizar Funcionario', 'ActionCancel': 'Funcionario_list'})

@login_required    
@permission_required('produtos.delete_funcionario') 
def Funcionario_delete(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == 'POST':
        funcionario.delete()
        return redirect('Funcionario_list')
    else:
        return render(request, 'generico/form_delete.html', {'delete': funcionario, 'model_name':'Deletar Funcionario', 'ActionCancel': 'Funcionario_list'})


@login_required    
@permission_required('produtos.view_localizacao') 
def Localizacao_list(request):

    if request.GET.get("list"):
        set_list_value_in_cache(int(request.GET.get("list")))

        return redirect('Localizacao_list')
    
    else:
        Qtlist = get_list_value_from_cache()

    model_list = Localizacao.objects.all()
    paginator = Paginator(model_list, Qtlist) 

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'model_name': 'Localização',
        'object_list': page_obj,
        'ActionAdd': ListAction(url_name='Localizacao_create', label='Adicionar Localização', icon='fa fa-plus', cor='w3-green'),
        'list_actions': [
            ListAction(url_name='Localizacao_edit', label='Atualizar', icon='fa fa-edit', cor='w3-blue'),
            ListAction(url_name='Localizacao_delete', label='Excluir', icon='fa fa-trash', cor='w3-red'),
        ],
        'column_titles' : [f.name for f in Localizacao._meta.fields],
        'get_attribute': get_attribute,
    }
    return render(request, 'generico/base_list.html', context)

@login_required    
@permission_required('produtos.add_localizacao') 
def Localizacao_create(request):
    if request.method == 'POST':
        try:
            form = LocalizacaoForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, "Atualização realizada com sucesso!")

                    return redirect('Localizacao_list')
                        
                except Exception as e:
                    messages.warning(request, "Erro ao validar dados, por favor preencha corretamente ou tente novamente mais tarde!")
                    return redirect('Localizacao_list')
        except Exception as e:
            messages.warning(request, "Erro por favor tente novamente mais tarde!")
            return redirect('Localizacao_list')
    else:
        form = LocalizacaoForm()
    return render(request, 'generico/form.html', {'form': form, 'model_name':'Cadastro de Localização', 'ActionCancel': 'Localizacao_list'})

@login_required    
@permission_required('produtos.change_localizacao') 
def Localizacao_edit(request, pk):
    localizacao = get_object_or_404(Localizacao, pk=pk)
    if request.method == 'POST':
        try:
            form = LocalizacaoForm(request.POST, request.FILES, instance=localizacao)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, "Atualização realizada com sucesso!")

                    return redirect('Localizacao_list')
                            
                except Exception as e:
                    messages.warning(request, "Erro ao validar dados, por favor preencha corretamente ou tente novamente mais tarde!")
                    return redirect('Localizacao_list')
        except Exception as e:
            messages.warning(request, "Erro por favor tente novamente mais tarde!")
            return redirect('Localizacao_list')
    else:
        form = LocalizacaoForm(instance=localizacao)
    return render(request, 'generico/form.html', {'form': form, 'model_name':'Atualizar Localização', 'ActionCancel': 'Localizacao_list'})

@login_required    
@permission_required('produtos.delete_localizacao') 
def Localizacao_delete(request, pk):
    localizacao = get_object_or_404(Localizacao, pk=pk)
    if request.method == 'POST':
        try:
            localizacao.delete()
            messages.success(request, "Exclusão realizada com sucesso!")
            return redirect('Localizacao_list')
        except Exception as e:
            messages.warning(request, "Erro por favor tente novamente mais tarde!")
            return redirect('Localizacao_list')
    else:
        return render(request, 'generico/form_delete.html', {'delete': localizacao, 'model_name':'Deletar Localização', 'ActionCancel': 'Localizacao_list'})


@login_required    
@permission_required('produtos.view_ordemcompra') 
def ordem_compra_list(request):

    if request.GET.get("list"):
        set_list_value_in_cache(int(request.GET.get("list")))

        return redirect('ordem_compra_list')
    
    else:
        Qtlist = get_list_value_from_cache()
 
    model_list = OrdemCompra.objects.all()
    paginator = Paginator(model_list, Qtlist) 

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'model_name': 'Ordens de Compras',
        'object_list': page_obj,
        'ActionAdd': ListAction(url_name='adicionar_ordem_compra', label='Adicionar Ordem de Compra', icon='fa fa-plus', cor='w3-green'),
        'list_actions': [
            ListAction(url_name='editar_ordem_compra', label='Atualizar', icon='fa fa-edit', cor='w3-blue'),
            ListAction(url_name='deletar_ordem_compra', label='Excluir', icon='fa fa-trash', cor='w3-red'),
        ],
        'column_titles' : [f.name for f in OrdemCompra._meta.fields],
        'get_attribute': get_attribute,
    }
    return render(request, 'generico/base_list.html', context)

@login_required    
@permission_required('produtos.add_ordemcompra') 
def adicionar_ordem_compra(request, extra=None):
    if request.method == 'POST':

        try:
            ordem_compra_form = OrdemCompraForm(request.POST)
            item_formset = ItemOrdemCompraFormSet(request.POST)

            if ordem_compra_form.is_valid() and item_formset.is_valid():
                    try:
                        ordem_compra = ordem_compra_form.save()
                        
                        for form in item_formset:
                            item = form.save(commit=False)
                            item.ordem_compra = ordem_compra
                                
                            item.save()
                            messages.success(request, "Atualização realizada com sucesso!")

                        return redirect('ordem_compra_list')
                    
                    except Exception as e:
                        messages.warning(request, "Erro ao validar dados, por favor preencha corretamente ou tente novamente mais tarde!")
                        return redirect('ordem_compra_list')
        except Exception as e:
            messages.warning(request, "Erro por favor tente novamente mais tarde!")
            return redirect('ordem_compra_list')
    else:
        ordem_compra_form = OrdemCompraForm()
        item_formset = ItemOrdemCompraFormSet()
        if extra:
            item_formset.extra = extra
        ExtraInclement = item_formset.extra + 1
        ExtraDeclement = item_formset.extra - 1

        return render(request, 'generico/formCompras.html', {'form': ordem_compra_form, 'item_formset': item_formset,'ItensForms': Produto.objects.all(), 'ActionCancel': 'ordem_compra_list','ExtraInclement': ExtraInclement,'ExtraDeclement':ExtraDeclement})

@login_required    
@permission_required('produtos.change_ordemcompra') 
def editar_ordem_compra(request, pk, extra=None):
    ordem_compra = get_object_or_404(OrdemCompra, pk=pk)

    if request.method == 'POST':
        try:
            ordem_compra_form = OrdemCompraForm(request.POST, instance=ordem_compra)
            item_formset = ItemOrdemCompraFormSet(request.POST, instance=ordem_compra)
            
            if ordem_compra_form.is_valid() and item_formset.is_valid():
                try:
                    ordem_compra_form.save()
                    
                    # Salvando manualmente o formulário filho
                    items = item_formset.save(commit=False)
                    
                    for item in items:
                        item.ordem_compra = ordem_compra
                            
                        item.save()
                    messages.success(request, "Atualização realizada com sucesso!")

                    return redirect('ordem_compra_list')
                
                except Exception as e:
                    messages.warning(request, "Erro ao validar dados, por favor preencha corretamente ou tente novamente mais tarde!")
                    return redirect('ordem_compra_list')
        except Exception as e:
            messages.warning(request, "Erro por favor tente novamente mais tarde!")
            return redirect('ordem_compra_list')

    else:
        ordem_compra_form = OrdemCompraForm(instance=ordem_compra)
        item_formset = ItemOrdemCompraFormSet(instance=ordem_compra)
        
        if extra:
            item_formset.extra = extra
        else:
            item_formset.extra = 0

        ExtraInclement = item_formset.extra + 1
        ExtraDeclement = item_formset.extra - 1


        return render(request, 'generico/formCompras_update.html', {'form': ordem_compra_form, 'item_formset': item_formset, 'ItensForms': Produto.objects.all(), 'ActionCancel': 'ordem_compra_list','ExtraInclement': ExtraInclement,'ExtraDeclement':ExtraDeclement, 'pk':pk})

@login_required    
@permission_required('produtos.delete_itemordemcompra') 
def deletar_itemordem_compra(request, pk):
    ItemOrdemCompras = get_object_or_404(ItemOrdemCompra, pk=pk)
    ItemOrdemCompras.delete()
    back = request.GET.get("back")
    return redirect(back)

@login_required    
@permission_required('produtos.delete_ordemcompra') 
def deletar_ordem_compra(request, pk):
    ordem_compra = get_object_or_404(OrdemCompra, pk=pk)
    if request.method == 'POST':
        try:
            ordem_compra.delete()
            messages.success(request, "Exclusão realizada com sucesso!")
            return redirect('ordem_compra_list')
        except Exception as e:
            messages.warning(request, "Erro por favor tente novamente mais tarde!")
            return redirect('ordem_compra_list')
    else:
        return render(request, 'generico/form_delete.html', {'delete': ordem_compra, 'model_name':'Deletar Ordem de Compra', 'ActionCancel': 'ordem_compra_list'})

@login_required    
@permission_required('produtos.view_ordemvenda') 
def ordem_venda_list(request):

    if request.GET.get("list"):
        set_list_value_in_cache(int(request.GET.get("list")))

        return redirect('ordem_venda_list')
    
    else:
        Qtlist = get_list_value_from_cache()

    model_list = OrdemVenda.objects.all()
    paginator = Paginator(model_list, Qtlist) 

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'model_name': 'Ordens de Venda',
        'object_list': page_obj,
        'ActionAdd': ListAction(url_name='adicionar_ordem_venda', label='Adicionar Ordem de Venda', icon='fa fa-plus', cor='w3-green'),
        'list_actions': [
            ListAction(url_name='editar_ordem_venda', label='Atualizar', icon='fa fa-edit', cor='w3-blue'),
            ListAction(url_name='deletar_ordem_venda', label='Excluir', icon='fa fa-trash', cor='w3-red'),
        ],
        'column_titles' : [f.name for f in OrdemVenda._meta.fields],
        'get_attribute': get_attribute,
    }
    return render(request, 'generico/base_list.html',  context)

@login_required    
@permission_required('produtos.add_ordemvenda') 
def adicionar_ordem_venda(request, extra=None):
    if request.method == 'POST':

        try:
            ordem_venda_form = OrdemVendaForm(request.POST)
            item_formset = ItemOrdemVendaFormSet(request.POST)

            if ordem_venda_form.is_valid() and item_formset.is_valid():
                try:
                    ordem_venda = ordem_venda_form.save()
                    
                    for form in item_formset:
                        item = form.save(commit=False)
                        item.ordem_venda = ordem_venda
                            
                        item.save()

                        messages.success(request, "Atualização realizada com sucesso!")

                        return redirect('ordem_venda_list')
                except Exception as e:
                    messages.warning(request, "Erro na atualização dos dados Por favor, preencha os dados corretamente ou tente novamente mais tarde!")
                    return redirect('ordem_venda_list')
        except Exception as e:
            messages.warning(request, "Erro por favor tente novamente mais tarde!")
            return redirect('ordem_venda_list')
    else:
        ordem_venda_form = OrdemVendaForm()
        item_formset = ItemOrdemVendaFormSet()
        if extra:
            item_formset.extra = extra
        ExtraInclement = item_formset.extra + 1
        ExtraDeclement = item_formset.extra - 1

        return render(request, 'generico/formVenda.html', {'form': ordem_venda_form, 'item_formset': item_formset,'ItensForms': Produto.objects.all(), 'ActionCancel': 'ordem_venda_list', 'model_name':'Ordens de Vendas','ExtraInclement': ExtraInclement,'ExtraDeclement':ExtraDeclement})

@login_required    
@permission_required('produtos.change_ordemvenda') 
def editar_ordem_venda(request, pk, extra=None):
    ordem_venda = get_object_or_404(OrdemVenda, pk=pk)

    if request.method == 'POST':
        try:
            ordem_venda_form = OrdemVendaForm(request.POST, instance=ordem_venda)
            item_formset = ItemOrdemVendaFormSet(request.POST, instance=ordem_venda)

        
            if ordem_venda_form.is_valid() and item_formset.is_valid():
                try:
                    ordem_venda_form.save()

                    # Salvando manualmente o formulário filho
                    items = item_formset.save(commit=False)
                    
                    for item in items:
                        item.ordem_venda = ordem_venda
                        item.save()
                    messages.success(request, "Atualização realizada com sucesso!")

                    return redirect('ordem_venda_list')
                except Exception as e:
                    messages.warning(request, "Erro na atualização dos dados Por favor, preencha os dados corretamente ou tente novamente mais tarde!")
                    return redirect('ordem_venda_list')
        except Exception as e:
            messages.warning(request, "Erro por favor tente novamente mais tarde!")
            return redirect('ordem_venda_list')

    else:
        ordem_venda_form = OrdemVendaForm(instance=ordem_venda)
        item_formset = ItemOrdemVendaFormSet(instance=ordem_venda)
        
        if extra:
            item_formset.extra = extra
        else:
            item_formset.extra = 0

        ExtraInclement = item_formset.extra + 1
        ExtraDeclement = item_formset.extra - 1


        return render(request, 'generico/formVenda_update.html', {'form': ordem_venda_form, 'item_formset': item_formset, 'ItensForms': Produto.objects.all(), 'ActionCancel': 'ordem_venda_list', 'model_name':'Ordens de Vendas','ExtraInclement': ExtraInclement,'ExtraDeclement':ExtraDeclement, 'pk':pk})

@login_required    
@permission_required('produtos.delete_itemordemvenda') 
def deletar_itemordem_venda(request, pk):
    ItemOrdemVendas = get_object_or_404(ItemOrdemVenda, pk=pk)
    ItemOrdemVendas.delete()
    back = request.GET.get("back")
    return redirect(back)

@login_required    
@permission_required('produtos.delete_ordemvenda') 
def deletar_ordem_venda(request, pk):
    OrdemVendas = get_object_or_404(OrdemVenda, pk=pk)
    if request.method == 'POST':
        try:
            OrdemVendas.delete()
            messages.success(request, "Exclusão realizada com sucesso!")
            return redirect('ordem_venda_list')
        except Exception as e:
            messages.warning(request, "Erro por favor tente novamente mais tarde!")
            return redirect('ordem_compra_list')
    else:
        return render(request, 'generico/form_delete.html', {'delete': OrdemVendas, 'model_name':'Deletar Ordem de Venda', 'ActionCancel': 'ordem_venda_list'})


@login_required    
@permission_required('produtos.view_configuracaosistema') 
def configuracao_sistema_list(request):

    if request.GET.get("list"):
        set_list_value_in_cache(int(request.GET.get("list")))

        return redirect('configuracao_sistema_list')
    
    else:
        Qtlist = get_list_value_from_cache()
     
    model_list = ConfiguracaoSistema.objects.all()
    paginator = Paginator(model_list, Qtlist) 

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'model_name': 'Configuração de Sistema',
        'object_list': page_obj,
        'list_actions': [
            ListAction(url_name='editar_configuracao_sistema', label='Atualizar', icon='fa fa-edit', cor='w3-blue'),
        ],
        'column_titles' : [f.name for f in ConfiguracaoSistema._meta.fields],
        'get_attribute': get_attribute,
    }
    return render(request, 'generico/base_list.html',  context)

@login_required    
@permission_required('produtos.change_configuracaosistema')
def editar_configuracao_sistema(request, pk):
    configuracao = get_object_or_404(ConfiguracaoSistema, pk=pk)
    if request.method == 'POST':
        try:
            ConfiguracaoSistema_form = ConfiguracaoSistemaForm(request.POST, instance=configuracao)
            if ConfiguracaoSistema_form.is_valid():
                try:
                    ConfiguracaoSistema_form.save()
                    messages.success(request, "Atualização realizada com sucesso!")
                    return redirect('configuracao_sistema_list')
                    
                except Exception as e:
                    messages.warning(request, "Erro ao validar dados, por favor preencha corretamente ou tente novamente mais tarde!")
                    return redirect('ordem_compra_list')
        except Exception as e:
            messages.warning(request, "Erro por favor tente novamente mais tarde!")
            return redirect('ordem_compra_list')
    else:
        ConfiguracaoSistema_form = ConfiguracaoSistemaForm(instance=configuracao)
        context = {
            'fieldName' : [],
        }


    return render(request, 'generico/form.html', {'form': ConfiguracaoSistema_form, 'a': context, 'model_name':'Configuração de Sistema', 'ActionCancel': 'configuracao_sistema_list'})

# def deletar_configuracao_sistema(request, pk):
#     configuracao = get_object_or_404(ConfiguracaoSistema, pk=pk)
#     configuracao.delete()
#     return redirect('configuracao_sistema_list')

# def adicionar_configuracao_sistema(request):
#     if request.method == 'POST':
#         form = ConfiguracaoSistemaForm(request.POST)
        
#         if form.is_valid():
#             form.save()
#             return redirect('configuracao_sistema_list')
#     else:
#         form = ConfiguracaoSistemaForm()
#         context = {
#             'fieldName' : [],
#         }

#     return render(request, 'generico/form.html', {'form': form, 'a': context, 'model_name':'Configuracao do Sistema', 'ActionCancel': 'lista_produtos'})

