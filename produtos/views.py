import logging
import logging.config
import secrets
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from services.Notas_service import NotasService
from .forms import *
from django.forms import formset_factory
from .models import *
from .utils import *
from .fields import *
from django.core.paginator import Paginator
from django.core.cache import cache
from django.contrib.auth.decorators import  login_required, permission_required
from django.http import HttpResponse, Http404

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

@login_required
def dashboard(request):
    user_profiles = UserProfile.objects.filter(user=request.user)

    # Verifique se o queryset está vazio
    if user_profiles.exists():
        UserProfiles = user_profiles.first()
    else:
        UserProfiles = None 
        
    context = {
        'UserProfiles': UserProfiles,
    }
    return render(request, 'dashboard.html', context)

@permission_required('produtos.view_produto',raise_exception=True)
@login_required
def produto_list(request):
    
    if request.GET.get("list") and request.GET.get("list").isdigit():
        set_list_value_in_cache(int(request.GET.get("list")))
        Qtlist = 20

        return redirect('lista_produtos')
    
    else:
        Qtlist = get_list_value_from_cache()
    
    

    model_list = Produto.objects.all()
    paginator = Paginator(model_list, Qtlist) 
    

    user_profiles = UserProfile.objects.filter(user=request.user)

    # Verifique se o queryset está vazio
    if user_profiles.exists():
        UserProfiles = user_profiles.first()
    else:
        UserProfiles = None 


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
        
            user_profiles = UserProfile.objects.filter(user=request.user)

            # Verifique se o queryset está vazio
            if user_profiles.exists():
                UserProfiles = user_profiles.first()
            else:
                UserProfiles = None

            context = {
                'form': form,
                'UserProfiles': UserProfiles,
                'model_name':'Cadastro de Produto',
                'ActionCancel': 'lista_produtos',
                'fieldName' : [
                    ListAction(id=2,url_name='Categoria_list', name='categoria', label='Visualizar', icon='fa fa-edit', cor='w3-blue'), 
                    ListAction(id=4,url_name='Marca_list', name='marca', label='Visualizar', icon='fa fa-edit', cor='w3-blue'),  
                    ListAction(id=6,url_name='Unidade_list', name='unidade', label='Visualizar', icon='fa fa-edit', cor='w3-blue'),
                ],
            }

            return render(request, 'generico/form.html', context)


@login_required
@permission_required('produtos.change_produto',raise_exception=True)
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
            
            user_profiles = UserProfile.objects.filter(user=request.user)

            # Verifique se o queryset está vazio
            if user_profiles.exists():
                UserProfiles = user_profiles.first()
            else:
                UserProfiles = None

            context = {
                'form': form,
                'UserProfiles': UserProfiles,
                'model_name':'Atualizar Produto',
                'ActionCancel': 'lista_produtos',
                'fieldName' : [  
                    ListAction(id=2,url_name='Categoria_list', name='categoria', label='Visualizar', icon='fa fa-search', cor='w3-blue'),  
                    ListAction(id=4,url_name='Marca_list', name='marca', label='visualizar', icon='fa fa-search', cor='w3-blue'),    
                    ListAction(id=6,url_name='Unidade_list', name='unidade', label='visualizar', icon='fa fa-search', cor='w3-blue'),
                ],
            }

            return render(request, 'generico/form.html', context)

@login_required
@permission_required('produtos.delete_produto',raise_exception=True)
def produto_delete(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        return redirect('lista_produtos')
    else:
        form = ProdutoForm(instance=produto)

        user_profiles = UserProfile.objects.filter(user=request.user)

        # Verifique se o queryset está vazio
        if user_profiles.exists():
            UserProfiles = user_profiles.first()
        else:
            UserProfiles = None

        context = {
            'form': form,
            'UserProfiles': UserProfiles,
            'delete': produto,
            'model_name':'Deletar Produto',
            'ActionCancel': 'lista_produtos',
            'fieldName' : [],
        }
    return render(request, 'generico/form_delete.html', context)


@login_required
@permission_required('produtos.view_categoria',raise_exception=True)
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

    user_profiles = UserProfile.objects.filter(user=request.user)

    # Verifique se o queryset está vazio
    if user_profiles.exists():
        UserProfiles = user_profiles.first()
    else:
        UserProfiles = None

    context = {
        'model_name': 'Categoria',
        'UserProfiles': UserProfiles,
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
@permission_required('produtos.add_categoria',raise_exception=True)
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

        user_profiles = UserProfile.objects.filter(user=request.user)

        # Verifique se o queryset está vazio
        if user_profiles.exists():
            UserProfiles = user_profiles.first()
        else:
            UserProfiles = None

        context = {
            'form': form,
            'UserProfiles': UserProfiles,
            'model_name':'Cadastro de Categoria',
            'ActionCancel': 'Categoria_list',
            'fieldName' : [],
        }

    return render(request, 'generico/form.html', context)

@login_required
@permission_required('produtos.change_categoria',raise_exception=True)
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

        user_profiles = UserProfile.objects.filter(user=request.user)

        # Verifique se o queryset está vazio
        if user_profiles.exists():
            UserProfiles = user_profiles.first()
        else:
            UserProfiles = None
        
        context = {
            'form': form,
            'UserProfiles': UserProfiles,
            'model_name':'Atualizar Categoria',
            'ActionCancel': 'Categoria_list',
            'fieldName' : [],
        }

    return render(request, 'generico/form.html', context)

@login_required
@permission_required('produtos.delete_categoria',raise_exception=True)
def Categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('Categoria_list')
    else:

        user_profiles = UserProfile.objects.filter(user=request.user)

        # Verifique se o queryset está vazio
        if user_profiles.exists():
            UserProfiles = user_profiles.first()
        else:
            UserProfiles = None
        
        context = {
            'UserProfiles': UserProfiles,
            'delete': categoria, 
            'model_name':'Deletar Categoria',
            'ActionCancel': 'Categoria_list',
            'fieldName' : [],
        }
        return render(request, 'generico/form_delete.html', context)

@login_required    
@permission_required('produtos.view_promocao',raise_exception=True)  
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
@permission_required('produtos.add_promocao',raise_exception=True) 
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
@permission_required('produtos.change_promocao',raise_exception=True) 
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
@permission_required('produtos.delete_promocao',raise_exception=True) 
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
@permission_required('produtos.view_unidade',raise_exception=True) 
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
    
    user_profiles = UserProfile.objects.filter(user=request.user)

    # Verifique se o queryset está vazio
    if user_profiles.exists():
        UserProfiles = user_profiles.first()
    else:
        UserProfiles = None

    context = {
        'model_name': 'Unidade',
        'UserProfiles': UserProfiles,
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
@permission_required('produtos.add_unidade',raise_exception=True) 
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

        user_profiles = UserProfile.objects.filter(user=request.user)

        # Verifique se o queryset está vazio
        if user_profiles.exists():
            UserProfiles = user_profiles.first()
        else:
            UserProfiles = None

        context = {
            'form': form, 
            'UserProfiles': UserProfiles,
            'model_name':'Cadastro de Unidade',
            'ActionCancel': 'Unidade_list',
            'fieldName' : [],
        }
        
    return render(request, 'generico/form.html', context)

@login_required    
@permission_required('produtos.change_unidade',raise_exception=True) 
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

        user_profiles = UserProfile.objects.filter(user=request.user)

        # Verifique se o queryset está vazio
        if user_profiles.exists():
            UserProfiles = user_profiles.first()
        else:
            UserProfiles = None

        context = {
            'form': form, 
            'UserProfiles': UserProfiles,
            'model_name':'Atualizar Unidade',
            'ActionCancel': 'Unidade_list',
            'fieldName' : [],
        }

        return render(request, 'generico/form.html', context)

@login_required    
@permission_required('produtos.delete_unidade',raise_exception=True) 
def Unidade_delete(request, pk):
    unidade = get_object_or_404(Unidade, pk=pk)
    if request.method == 'POST':
        unidade.delete()
        return redirect('Unidade_list')
    else:
        
        user_profiles = UserProfile.objects.filter(user=request.user)

        # Verifique se o queryset está vazio
        if user_profiles.exists():
            UserProfiles = user_profiles.first()
        else:
            UserProfiles = None
        
        context = {
            'UserProfiles': UserProfiles,
            'delete': unidade,
            'model_name':'Deletar Unidade',
            'ActionCancel': 'Unidade_list',
            'fieldName' : [],
        }

        return render(request, 'generico/form_delete.html', context)



@login_required    
@permission_required('produtos.view_marca',raise_exception=True) 
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

    user_profiles = UserProfile.objects.filter(user=request.user)

    # Verifique se o queryset está vazio
    if user_profiles.exists():
        UserProfiles = user_profiles.first()
    else:
        UserProfiles = None

    context = {
        'model_name': 'Marca',
        'UserProfiles': UserProfiles,
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
@permission_required('produtos.add_marca',raise_exception=True) 
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

        user_profiles = UserProfile.objects.filter(user=request.user)

        # Verifique se o queryset está vazio
        if user_profiles.exists():
            UserProfiles = user_profiles.first()
        else:
            UserProfiles = None
        
        context = {
            'form': form,
            'UserProfiles': UserProfiles,
            'model_name':'Cadastro de Marca',
            'ActionCancel': 'Marca_list',
            'fieldName' : [],
        }

        return render(request, 'generico/form.html', context)

@login_required    
@permission_required('produtos.change_marca',raise_exception=True) 
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

        user_profiles = UserProfile.objects.filter(user=request.user)

        # Verifique se o queryset está vazio
        if user_profiles.exists():
            UserProfiles = user_profiles.first()
        else:
            UserProfiles = None

        context = {
            'form': form,
            'UserProfiles': UserProfiles,
            'model_name':'Atualizar Marca',
            'ActionCancel': 'Marca_list',
            'fieldName' : [],
        }

        return render(request, 'generico/form.html', context)

@login_required    
@permission_required('produtos.delete_marca',raise_exception=True) 
def Marca_delete(request, pk):
    marca = get_object_or_404(Marca, pk=pk)
    if request.method == 'POST':
        marca.delete()
        return redirect('Marca_list')
    else:
        
        user_profiles = UserProfile.objects.filter(user=request.user)

        # Verifique se o queryset está vazio
        if user_profiles.exists():
            UserProfiles = user_profiles.first()
        else:
            UserProfiles = None

        context = {
            'UserProfiles': UserProfiles,
            'delete': marca,
            'model_name':'Deletar Marca',
            'ActionCancel': 'Marca_list',
            'fieldName' : [],
        }
        return render(request, 'generico/form_delete.html', context)



# @login_required    
# @permission_required('produtos.view_fornecedor',raise_exception=True) 
# def Fornecedor_list(request):

#     if request.GET.get("list"):
#         set_list_value_in_cache(int(request.GET.get("list")))

#         return redirect('Fornecedor_list')
    
#     else:
#         Qtlist = get_list_value_from_cache()

#     user_profiles = UserProfile.objects.filter(user=request.user)

#     # Verifique se o queryset está vazio
#     if user_profiles.exists():
#         UserProfiles = user_profiles.first()
#     else:
#         UserProfiles = None 

#     model_list = Fornecedor.objects.all()
#     paginator = Paginator(model_list, Qtlist) 

#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     context = {
#         'UserProfiles': UserProfiles,
#         'model_name': 'Fornecedor',
#         'object_list': page_obj,
#         'ActionAdd': ListAction(url_name='Fornecedor_create', label='Adicionar Fornecedor', icon='fa fa-plus', cor='w3-green'),
#         'list_actions': [
#             ListAction(url_name='Fornecedor_edit', label='Atualizar', icon='fa fa-edit', cor='w3-blue'),
#             ListAction(url_name='Fornecedor_delete', label='Excluir', icon='fa fa-trash', cor='w3-red'),
#         ],
#         'column_titles' : [f.name for f in Fornecedor._meta.fields],
#         'get_attribute': get_attribute,
#     }
#     return render(request, 'generico/base_list.html', context)

# @login_required    
# @permission_required('produtos.add_fornecedor',raise_exception=True) 
# def Fornecedor_create(request):
#     if request.method == 'POST':
#         try:
#             form = FornecedorForm(request.POST, request.FILES)
#             if form.is_valid():
#                 try:
#                     form.save()
            
#                     messages.success(request, "Atualização realizada com sucesso!")

#                     return redirect('Fornecedor_list')
                        
#                 except Exception as e:
#                     messages.warning(request, "Erro ao validar dados, por favor preencha corretamente ou tente novamente mais tarde!")
#                     return redirect('Fornecedor_list')
#         except Exception as e:
#             messages.warning(request, "Erro por favor tente novamente mais tarde!")
#             return redirect('Fornecedor_list')
#     else:
#         form = FornecedorForm()

#         user_profiles = UserProfile.objects.filter(user=request.user)

#         # Verifique se o queryset está vazio
#         if user_profiles.exists():
#             UserProfiles = user_profiles.first()
#         else:
#             UserProfiles = None 

#         context = {
#             'form': form,
#             'UserProfiles': UserProfiles,
#             'model_name':'Cadastro de Fornecedor',
#             'ActionCancel': 'Fornecedor_list',
#             'fieldName' : [],
#         }

#     return render(request, 'generico/form.html', context)

# @login_required    
# @permission_required('produtos.change_fornecedor',raise_exception=True) 
# def Fornecedor_edit(request, pk):
#     fornecedor = get_object_or_404(Fornecedor, pk=pk)
#     if request.method == 'POST':
#         try:    
#             form = FornecedorForm(request.POST, request.FILES, instance=fornecedor)
#             if form.is_valid():
#                 try:
#                     form.save()
#                     messages.success(request, "Atualização realizada com sucesso!")

#                     return redirect('Fornecedor_list')
                            
#                 except Exception as e:
#                     messages.warning(request, "Erro ao validar dados, por favor preencha corretamente ou tente novamente mais tarde!")
#                     return redirect('Fornecedor_list')
#         except Exception as e:
#             messages.warning(request, "Erro por favor tente novamente mais tarde!")
#             return redirect('Fornecedor_list')
        
#     else:
#         form = FornecedorForm(instance=fornecedor)
        
#         user_profiles = UserProfile.objects.filter(user=request.user)

#         # Verifique se o queryset está vazio
#         if user_profiles.exists():
#             UserProfiles = user_profiles.first()
#         else:
#             UserProfiles = None 

#         context = {
#             'form': form,
#             'UserProfiles': UserProfiles,
#             'model_name':'Atualizar Fornecedor',
#             'ActionCancel': 'Fornecedor_list',
#             'fieldName' : [],
#         }
        
#         return render(request, 'generico/form.html', context)

# @login_required    
# @permission_required('produtos.delete_fornecedor',raise_exception=True) 
# def Fornecedor_delete(request, pk):
#     fornecedor = get_object_or_404(Fornecedor, pk=pk)
#     if request.method == 'POST':
#         fornecedor.delete()
#         return redirect('Fornecedor_list')
#     else:
        
#         user_profiles = UserProfile.objects.filter(user=request.user)

#         # Verifique se o queryset está vazio
#         if user_profiles.exists():
#             UserProfiles = user_profiles.first()
#         else:
#             UserProfiles = None 

#         context = {
#             'UserProfiles': UserProfiles,
#             'delete': fornecedor,
#             'model_name':'Deletar Fornecedor',
#             'ActionCancel': 'Fornecedor_list',
#             'fieldName' : [],
#         }
#         return render(request, 'generico/form_delete.html', context)



# @login_required    
# @permission_required('produtos.view_funcionario',raise_exception=True) 
# def Funcionario_list(request):

#     if request.GET.get("list"):
#         set_list_value_in_cache(int(request.GET.get("list")))

#         return redirect('Funcionario_list')
    
#     else:
#         Qtlist = get_list_value_from_cache()

#     model_list = Funcionario.objects.all()
#     paginator = Paginator(model_list, Qtlist) 

#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     user_profiles = UserProfile.objects.filter(user=request.user)

#     # Verifique se o queryset está vazio
#     if user_profiles.exists():
#         UserProfiles = user_profiles.first()
#     else:
#         UserProfiles = None

#     context = {
#         'model_name': 'Funcionario',
#         'UserProfiles': UserProfiles,
#         'object_list': page_obj,
#         'ActionAdd': ListAction(url_name='Funcionario_create', label='Adicionar Funcionario', icon='fa fa-plus', cor='w3-green'),
#         'list_actions': [
#             ListAction(url_name='Funcionario_edit', label='Atualizar', icon='fa fa-edit', cor='w3-blue'),
#             ListAction(url_name='Funcionario_delete', label='Excluir', icon='fa fa-trash', cor='w3-red'),
#         ],
#         'column_titles' : [f.name for f in Funcionario._meta.fields],
#         'get_attribute': get_attribute,
#     }
#     return render(request, 'generico/base_list.html', context)

# @login_required    
# @permission_required('produtos.add_funcionario',raise_exception=True) 
# def Funcionario_create(request):
#     if request.method == 'POST':
#         try:
#             form = FuncionarioForm(request.POST, request.FILES)
            
#             if form.is_valid():
#                 try:
#                     form.save()
#                     messages.success(request, "Atualização realizada com sucesso!")

#                     return redirect('Funcionario_list')
                        
#                 except Exception as e:
#                     messages.warning(request, "Erro ao validar dados, por favor preencha corretamente ou tente novamente mais tarde!")
#                     return redirect('Funcionario_list')
#         except Exception as e:
#             messages.warning(request, "Erro por favor tente novamente mais tarde!")
#             return redirect('Funcionario_list')
#     else:
#         form = FuncionarioForm()
        
#         user_profiles = UserProfile.objects.filter(user=request.user)

#         # Verifique se o queryset está vazio
#         if user_profiles.exists():
#             UserProfiles = user_profiles.first()
#         else:
#             UserProfiles = None 

#         context = {
#             'form': form,
#             'UserProfiles': UserProfiles,
#             'model_name':'Cadastro de Funcionario',
#             'ActionCancel': 'Funcionario_list',
#             'fieldName' : [],
#         }
#     return render(request, 'generico/form.html', context)

# @login_required    
# @permission_required('produtos.change_funcionario',raise_exception=True) 
# def Funcionario_edit(request, pk):
#     funcionario = get_object_or_404(Funcionario, pk=pk)
#     if request.method == 'POST':
#         try:
#             form = FuncionarioForm(request.POST, request.FILES, instance=funcionario)
#             if form.is_valid():
#                 try:
#                     form.save()
#                     messages.success(request, "Atualização realizada com sucesso!")

#                     return redirect('Funcionario_list')
                            
#                 except Exception as e:
#                     messages.warning(request, "Erro ao validar dados, por favor preencha corretamente ou tente novamente mais tarde!")
#                     return redirect('Funcionario_list')
#         except Exception as e:
#             messages.warning(request, "Erro por favor tente novamente mais tarde!")
#             return redirect('Funcionario_list')
#     else:
#         form = FuncionarioForm(instance=funcionario)
        
#         user_profiles = UserProfile.objects.filter(user=request.user)

#         # Verifique se o queryset está vazio
#         if user_profiles.exists():
#             UserProfiles = user_profiles.first()
#         else:
#             UserProfiles = None 

#         context = {
#             'form': form,
#             'UserProfiles': UserProfiles,
#             'model_name':'Atualizar Funcionario',
#             'ActionCancel': 'Funcionario_list',
#             'fieldName' : [],
#         }
#         return render(request, 'generico/form.html', context)

# @login_required    
# @permission_required('produtos.delete_funcionario',raise_exception=True) 
# def Funcionario_delete(request, pk):
#     funcionario = get_object_or_404(Funcionario, pk=pk)
#     if request.method == 'POST':
#         funcionario.delete()
#         return redirect('Funcionario_list')
#     else:

#         user_profiles = UserProfile.objects.filter(user=request.user)

#         # Verifique se o queryset está vazio
#         if user_profiles.exists():
#             UserProfiles = user_profiles.first()
#         else:
#             UserProfiles = None 

#         context = {
#             'UserProfiles': UserProfiles,
#             'delete': funcionario,
#             'model_name':'Deletar Funcionario', 
#             'ActionCancel': 'Funcionario_list',
#             'fieldName' : [],
#         }
#         return render(request, 'generico/form_delete.html', context)


@login_required    
@permission_required('produtos.view_localizacao',raise_exception=True) 
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

    user_profiles = UserProfile.objects.filter(user=request.user)

    # Verifique se o queryset está vazio
    if user_profiles.exists():
        UserProfiles = user_profiles.first()
    else:
        UserProfiles = None

    context = {
        'model_name': 'Localização',
        'UserProfiles': UserProfiles,
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
@permission_required('produtos.add_localizacao',raise_exception=True) 
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

        user_profiles = UserProfile.objects.filter(user=request.user)

        # Verifique se o queryset está vazio
        if user_profiles.exists():
            UserProfiles = user_profiles.first()
        else:
            UserProfiles = None 

        context = {
            'form': form,
            'UserProfiles': UserProfiles,
            'model_name':'Cadastro de Localização', 
            'ActionCancel': 'Localizacao_list',
            'fieldName' : [],
        }
        return render(request, 'generico/form.html', context)

@login_required    
@permission_required('produtos.change_localizacao',raise_exception=True) 
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

        user_profiles = UserProfile.objects.filter(user=request.user)

        # Verifique se o queryset está vazio
        if user_profiles.exists():
            UserProfiles = user_profiles.first()
        else:
            UserProfiles = None 

        context = {
            'form': form,
            'UserProfiles': UserProfiles,
            'model_name':'Atualizar Localização', 
            'ActionCancel': 'Localizacao_list',
            'fieldName' : [],
        }
    return render(request, 'generico/form.html', context)

@login_required    
@permission_required('produtos.delete_localizacao',raise_exception=True) 
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

        
        user_profiles = UserProfile.objects.filter(user=request.user)

        # Verifique se o queryset está vazio
        if user_profiles.exists():
            UserProfiles = user_profiles.first()
        else:
            UserProfiles = None 

        context = {
            'UserProfiles': UserProfiles,
            'delete': localizacao,
            'model_name':'Deletar Localização', 
            'ActionCancel': 'Localizacao_list',
            'fieldName' : [],
        }

        return render(request, 'generico/form_delete.html', context)


@login_required    
@permission_required('produtos.view_ordemcompra',raise_exception=True) 
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

    user_profiles = UserProfile.objects.filter(user=request.user)

    # Verifique se o queryset está vazio
    if user_profiles.exists():
        UserProfiles = user_profiles.first()
    else:
        UserProfiles = None

    context = {
        'model_name': 'Ordens de Compras',
        'UserProfiles': UserProfiles,
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
@permission_required('produtos.add_ordemcompra',raise_exception=True) 
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

        user_profiles = UserProfile.objects.filter(user=request.user)

        # Verifique se o queryset está vazio
        if user_profiles.exists():
            UserProfiles = user_profiles.first()
        else:
            UserProfiles = None 

        context = {
            'form': ordem_compra_form,
            'UserProfiles': UserProfiles, 
            'item_formset': item_formset,
            'ItensForms': Produto.objects.all(), 
            'ActionCancel': 'ordem_compra_list',
            'ExtraInclement': ExtraInclement,
            'ExtraDeclement':ExtraDeclement
        }

        return render(request, 'generico/formCompras.html', context)

@login_required    
@permission_required('produtos.change_ordemcompra',raise_exception=True) 
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

        user_profiles = UserProfile.objects.filter(user=request.user)

        # Verifique se o queryset está vazio
        if user_profiles.exists():
            UserProfiles = user_profiles.first()
        else:
            UserProfiles = None 

        context = {
            'form': ordem_compra_form, 
            'UserProfiles': UserProfiles, 
            'item_formset': item_formset, 
            'ItensForms': Produto.objects.all(), 
            'ActionCancel': 'ordem_compra_list',
            'ExtraInclement': ExtraInclement,
            'ExtraDeclement':ExtraDeclement, 
            'pk':pk
        }

        return render(request, 'generico/formCompras_update.html', context)

@login_required    
@permission_required('produtos.delete_itemordemcompra',raise_exception=True) 
def deletar_itemordem_compra(request, pk):
    ItemOrdemCompras = get_object_or_404(ItemOrdemCompra, pk=pk)
    ItemOrdemCompras.delete()
    back = request.GET.get("back")
    return redirect(back)

@login_required    
@permission_required('produtos.delete_ordemcompra',raise_exception=True) 
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
        
        user_profiles = UserProfile.objects.filter(user=request.user)

        # Verifique se o queryset está vazio
        if user_profiles.exists():
            UserProfiles = user_profiles.first()
        else:
            UserProfiles = None 

        context = {
            'delete': ordem_compra, 
            'UserProfiles': UserProfiles,
            'model_name':'Deletar Ordem de Compra', 
            'ActionCancel': 'ordem_compra_list'
        }

        return render(request, 'generico/form_delete.html', context)

@login_required    
@permission_required('produtos.view_ordemvenda',raise_exception=True) 
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

    user_profiles = UserProfile.objects.filter(user=request.user)

    # Verifique se o queryset está vazio
    if user_profiles.exists():
        UserProfiles = user_profiles.first()
    else:
        UserProfiles = None 

    context = {
        'model_name': 'Ordens de Venda',
        'UserProfiles': UserProfiles,
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
@permission_required('produtos.add_ordemvenda',raise_exception=True) 
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

        user_profiles = UserProfile.objects.filter(user=request.user)

        # Verifique se o queryset está vazio
        if user_profiles.exists():
            UserProfiles = user_profiles.first()
        else:
            UserProfiles = None 

        context = {
            'form': ordem_venda_form, 
            'UserProfiles': UserProfiles,
            'item_formset': item_formset,
            'ItensForms': Produto.objects.all(), 
            'ActionCancel': 'ordem_venda_list', 
            'model_name':'Ordens de Vendas',
            'ExtraInclement': ExtraInclement,
            'ExtraDeclement':ExtraDeclement
        }
        return render(request, 'generico/formVenda.html', context)

@login_required    
@permission_required('produtos.change_ordemvenda',raise_exception=True) 
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

        user_profiles = UserProfile.objects.filter(user=request.user)

        # Verifique se o queryset está vazio
        if user_profiles.exists():
            UserProfiles = user_profiles.first()
        else:
            UserProfiles = None 

        context = {
            'form': ordem_venda_form, 
            'UserProfiles': UserProfiles,
            'item_formset': item_formset, 
            'ItensForms': Produto.objects.all(), 
            'ActionCancel': 'ordem_venda_list', 
            'model_name':'Ordens de Vendas',
            'ExtraInclement': ExtraInclement,
            'ExtraDeclement':ExtraDeclement, 
            'pk':pk
        }

        return render(request, 'generico/formVenda_update.html', context)

@login_required    
@permission_required('produtos.delete_itemordemvenda',raise_exception=True) 
def deletar_itemordem_venda(request, pk):
    ItemOrdemVendas = get_object_or_404(ItemOrdemVenda, pk=pk)
    ItemOrdemVendas.delete()
    back = request.GET.get("back")
    return redirect(back)

@login_required    
@permission_required('produtos.delete_ordemvenda',raise_exception=True) 
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

        user_profiles = UserProfile.objects.filter(user=request.user)

        # Verifique se o queryset está vazio
        if user_profiles.exists():
            UserProfiles = user_profiles.first()
        else:
            UserProfiles = None 

        context = {
            'delete': OrdemVendas, 
            'UserProfiles': UserProfiles,
            'model_name':'Deletar Ordem de Venda', 
            'ActionCancel': 'ordem_venda_list'
        }
        return render(request, 'generico/form_delete.html', context)


@login_required    
@permission_required('produtos.view_configuracaosistema',raise_exception=True) 
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
    
    user_profiles = UserProfile.objects.filter(user=request.user)

    # Verifique se o queryset está vazio
    if user_profiles.exists():
        UserProfiles = user_profiles.first()
    else:
        UserProfiles = None 


    context = {
        'model_name': 'Configuração de Sistema',
        'UserProfiles': UserProfiles,
        'object_list': page_obj,
        'ActionAdd': ListAction(url_name='adicionar_configuracao_sistema', label='adicionar configuração sistema', icon='fa fa-plus', cor='w3-green'),
        'list_actions': [
            ListAction(url_name='editar_configuracao_sistema', label='Atualizar', icon='fa fa-edit', cor='w3-blue'),
            ListAction(url_name='deletar_configuracao_sistema', label='Delete', icon='fa fa-trash', cor='w3-blue'),
        ],
        'column_titles' : [f.name for f in ConfiguracaoSistema._meta.fields],
        'get_attribute': get_attribute,
    }
    return render(request, 'generico/base_list.html',  context)

@login_required    
@permission_required('produtos.change_configuracaosistema',raise_exception=True)
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

        user_profiles = UserProfile.objects.filter(user=request.user)

        # Verifique se o queryset está vazio
        if user_profiles.exists():
            UserProfiles = user_profiles.first()
        else:
            UserProfiles = None 

        context = {
            'form': ConfiguracaoSistema_form,
            'UserProfiles': UserProfiles,
            'model_name':'Configuração de Sistema', 
            'ActionCancel': 'configuracao_sistema_list',
            'fieldName' : [],
        }
        

    return render(request, 'generico/form.html', context)

@login_required    
@permission_required('produtos.delete_configuracaosistema',raise_exception=True)

def deletar_configuracao_sistema(request, pk):
    configuracao = get_object_or_404(ConfiguracaoSistema, pk=pk)
    if request.method == 'POST':
        try:
            configuracao.delete()
            messages.success(request, "Exclusão realizada com sucesso!")
            return redirect('configuracao_sistema_list')
        except Exception as e:
            messages.warning(request, "Erro por favor tente novamente mais tarde!")
            return redirect('configuracao_sistema_list')
    else:

        user_profiles = UserProfile.objects.filter(user=request.user)

        # Verifique se o queryset está vazio
        if user_profiles.exists():
            UserProfiles = user_profiles.first()
        else:
            UserProfiles = None 

        context = {
            'delete': configuracao, 
            'UserProfiles': UserProfiles,
            'model_name':'Deletar Configuração de Sistema', 
            'ActionCancel': 'configuracao_sistema_list'
        }
        return render(request, 'generico/form_delete.html', context)


@login_required    
@permission_required('produtos.add_configuracaosistema',raise_exception=True)
def adicionar_configuracao_sistema(request):
    if request.method == 'POST':
        try:
            form = ConfiguracaoSistemaForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, "Atualização realizada com sucesso!")

                    return redirect('configuracao_sistema_list')
                        
                except Exception as e:
                    messages.warning(request, "Erro ao validar dados, por favor preencha corretamente ou tente novamente mais tarde!")
                    return redirect('configuracao_sistema_list')
        except Exception as e:
            messages.warning(request, "Erro por favor tente novamente mais tarde!")
            return redirect('configuracao_sistema_list')
    else:
        form = ConfiguracaoSistemaForm()

        user_profiles = UserProfile.objects.filter(user=request.user)

        # Verifique se o queryset está vazio
        if user_profiles.exists():
            UserProfiles = user_profiles.first()
        else:
            UserProfiles = None 

        context = {
            'form': form,
            'UserProfiles': UserProfiles,
            'model_name':'Configuracao do Sistema', 
            'ActionCancel': 'configuracao_sistema_list',
            'fieldName' : [],
        }
        return render(request, 'generico/form.html', context)


@login_required    
def home_notas(request):
    user_profiles = UserProfile.objects.filter(user=request.user)

    # Verifique se o queryset está vazio
    if user_profiles.exists():
        UserProfiles = user_profiles.first()
    else:
        UserProfiles = None 
        
    context = {
        'UserProfiles': UserProfiles,
    }
    return render(request, 'nfe/Home_Notas.html', context)

@login_required   
def home_nfe(request):
    user_profiles = UserProfile.objects.filter(user=request.user)

    # Verifique se o queryset está vazio
    if user_profiles.exists():
        UserProfiles = user_profiles.first()
    else:
        UserProfiles = None 
        
    context = {
        'UserProfiles': UserProfiles,
    }
    return render(request, 'nfe/home_nfe.html', context)

@login_required   
def emitir_nota(request):
    if request.method == 'POST':
        # Obter dados do formulário ou preparar o payload
        
        dados_nota = [
  {
    "idIntegracao": secrets.token_hex(15),
    "presencial": request.POST.get('presencial'),
    "consumidorFinal": request.POST.get('consumidorFinal'),
    "natureza": request.POST.get('natureza'),
    "emitente": {
      "cpfCnpj": request.POST.get('emitenteCpfCnpj')
    },
    "destinatario": {
      "cpfCnpj": request.POST.get('destinatarioCpfCnpj'),
      "razaoSocial": request.POST.get('razaoSocial'),
      "email": request.POST.get('email'),
      "endereco": {
        "tipoLogradouro": request.POST.get('tipoLogradouro'),
        "logradouro": request.POST.get('logradouro'),
        "numero": request.POST.get('numero'),
        "bairro": request.POST.get('bairro'),
        "codigoCidade": request.POST.get('codigoCidade'),
        "descricaoCidade": request.POST.get('descricaoCidade'),
        "estado": request.POST.get('estado'),
        "cep": request.POST.get('cep')
      }
    },
    "itens": [
      {
        "codigo": request.POST.get('codigo'),
        "descricao": request.POST.get('descricaoItem'),
        "ncm": request.POST.get('ncm'),
        "cest": request.POST.get('cest'),
        "cfop": request.POST.get('cfop'),
        "valorUnitario": {
          "comercial": request.POST.get('valorUnitarioComercial'),
          "tributavel": request.POST.get('valorUnitarioTributavel')
        },
        "valor": request.POST.get('valorPagamento'),
        "tributos": {
          "icms": {
            "origem": request.POST.get('origemIcms'),
            "cst": request.POST.get('cstIcms'),
            "baseCalculo": {
              "modalidadeDeterminacao": request.POST.get('modalidadeDeterminacaoBaseCalculo'),
              "valor": request.POST.get('valorBaseCalculoIcms')
            },
            "aliquota": request.POST.get('aliquotaIcms'),
            "valor": request.POST.get('valorIcms')
          },
          "pis": {
            "cst": request.POST.get('cstPis'),
            "baseCalculo": {
              "valor": request.POST.get('valorBaseCalculoPis'),
              "quantidade": request.POST.get('quantidadeBaseCalculoPis')
            },
            "aliquota": request.POST.get('aliquotaPis'),
            "valor": request.POST.get('valorPis')
          },
          "cofins": {
            "cst": f"{request.POST.get('cstCofins')}",
            "baseCalculo": {
              "valor": request.POST.get('valorBaseCalculoCofins')
            },
            "aliquota": request.POST.get('aliquotaCofins'),
            "valor": request.POST.get('valorCofins')
          }
        }
      }
    ],
    "pagamentos": [
      {
        "aVista": request.POST.get('aVista'),
        "meio": f'{request.POST.get('meioPagamento')}',
        "valor": request.POST.get('valorTotalPagamento')
      }
    ],
    "responsavelTecnico": {
      "cpfCnpj": request.POST.get('cpfCnpjResponsavel'),
      "nome": request.POST.get('nomeResponsavel'),
      "email": request.POST.get('emailResponsavel'),
      "telefone": {
        "ddd": request.POST.get('telefoneDdd'),
        "numero": request.POST.get('telefoneNumero')
      }
    }
  }
]

        
        plugnotas = NotasService()
        resultado = plugnotas.criar_nota_fiscal(dados_nota)
        print(resultado)
        return render(request, 'resultado.html', {'resultado': resultado})

    return render(request, 'emitir_nota.html')

@login_required   
def cancelar_nota(request):
    if request.method == 'POST':
        # Obter dados do formulário ou preparar o payload
        nota_id = request.POST.get('idIntegracao')
        motivo = "Erro na emissão da Nota Fiscal eletrônica."

        plugnotas = NotasService()
        resultado = plugnotas.cancelar_nota_fiscal(nota_id=nota_id,motivo= motivo)
        print(resultado)
        return render(request, 'resultadoCancelamento.html', {'resultado': resultado})

    return render(request, 'cancelar_nota.html')

@login_required   
def resumo_nota(request):
    if request.method == 'POST':
        # Obter dados do formulário ou preparar o payload
        nota_id = request.POST.get('id')
        plugnotas = NotasService()
        resultado = plugnotas.resumo_nota_fiscal(nota_id=nota_id)
        print(resultado)
        return render(request, 'resultadoResumo.html', {'resultado': resultado })

    return render(request, 'Resumo_nota.html')

@login_required   
def resumo_nota_idintegracao(request):
    if request.method == 'POST':
        # Obter dados do formulário ou preparar o payload
        idIntegracao = request.POST.get('idIntegracao')
        cnpj = request.POST.get('cnpj')

        plugnotas = NotasService()
        resultado = plugnotas.resumo_nota_fiscal_idintegracao(cnpj=cnpj, idIntegracao=idIntegracao)
        print(resultado)
        return render(request, 'resultadoResumo_idintegracao.html', {'resultado': resultado })

    return render(request, 'Resumo_nota_idintegracao.html')


@login_required   
def baixar_xml_cancelamento(request, nota_id):
    plugnotas = NotasService()
    response = plugnotas.baixar_xml_cancelamento(nota_id)

    if response.status_code == 200:
        # Retorna o XML para o usuário
        xml_content = response.content
        return HttpResponse(xml_content, content_type='application/xml')
    else:
        raise Http404("XML não encontrado ou erro ao processar a requisição.")

@login_required   
def baixar_cce_pdf(request, nota_id):
    plugnotas = NotasService()
    response = plugnotas.cce_baixar_pdf(nota_id)

    if response.status_code == 200:
        # Retorna o PDF para o usuário
        pdf_content = response.content
        return HttpResponse(pdf_content, content_type='application/pdf')
    else:
        raise Http404("PDF não encontrado ou erro ao processar a requisição.")


@login_required   
def baixar_cce_xml(request, nota_id):
    plugnotas = NotasService()
    response = plugnotas.cce_baixar_xml(nota_id)

    if response.status_code == 200:
        # Retorna o XML para o usuário
        xml_content = response.content
        return HttpResponse(xml_content, content_type='application/xml')
    else:
        raise Http404("XML não encontrado ou erro ao processar a requisição.")

@login_required   
def consultar_cancelamento_status_nota(request, nota_id):
        
        plugnotas = NotasService()
        resultado = plugnotas.consultar_cancelamento_status_nota_fiscal(nota_id=nota_id)
        print(resultado)
        return render(request, 'resultadoCancelamentoStatus.html', {'resultado': resultado, "nota_id": nota_id})

@login_required   
def consultar_correcao_status_nota(request):
    if request.method == 'POST':
        nota_id = request.POST.get('idIntegracao')    
        plugnotas = NotasService()
        resultado = plugnotas.consultar_correcao_status_nota_fiscal(nota_id=nota_id)
        print(resultado)
        return render(request, 'resultadoCorrecaoStatus.html', {'resultado': resultado, "nota_id": nota_id})
    return render(request, 'correcao_nota_status.html')

@login_required   
def criar_nota_fiscal(self, payload):
    try:
        url = f'{self.base_url}/nfe'
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()  # Lança exceção para erros HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'erro': f'Erro ao comunicar com a API: {str(e)}'}

@login_required   
def correcao_nota(request):
    if request.method == 'POST':
        # Obter dados do formulário ou preparar o payload
        nota_id = request.POST.get('idIntegracao')
        correcao = "Alterar o bairro do Destinatário para Bairro Teste"

        plugnotas = NotasService()
        resultado = plugnotas.correcao_nota_fiscal(nota_id=nota_id,correcao= correcao)
        print(resultado)
        return render(request, 'resultadoCorrecao.html', {'resultado': resultado})

    return render(request, 'correcao_nota.html')

@login_required   
def baixar_pdf(request, nota_id = None):
    if nota_id:
        plugnotas = NotasService()
        response = plugnotas.baixar_pdf(nota_id)

        if response.status_code == 200:
            # Retorna o PDF para o usuário
            pdf_content = response.content
            return HttpResponse(pdf_content, content_type='application/pdf')
        else:
            raise Http404("PDF não encontrado ou erro ao processar a requisição.")
    return render(request, 'baixar_pdf.html')

@login_required   
def baixar_xml(request, nota_id = None):
    if nota_id:
        plugnotas = NotasService()
        response = plugnotas.baixar_xml(nota_id)

        if response.status_code == 200:
            # Retorna o XML para o usuário
            xml_content = response.content
            return HttpResponse(xml_content, content_type='application/xml')
        else:
            raise Http404("XML não encontrado ou erro ao processar a requisição.")
    return render(request, 'baixar_xml.html')