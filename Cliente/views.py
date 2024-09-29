from django.shortcuts import render

from Cliente.fields import ListAction
from Cliente.forms import ClienteForm
from Cliente.models import Cliente
from Cliente.utils import get_attribute
from produtos.models import UserProfile
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.contrib import messages

from produtos.views import get_list_value_from_cache, set_list_value_in_cache


# Create your views here.
class Cliente_list(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Cliente
    template_name = 'generico/base_list_r.html'
    context_object_name = 'object_list'
    permission_required = 'Clientes.view_Cliente'
    raise_exception = True
    paginate_by = 1 # Valor padrão, caso o cache falhe

    def get_paginate_by(self, queryset):
        # Verifica se o valor de list está na URL e se é um número
        if self.request.GET.get("list") and self.request.GET.get("list").isdigit():
            list_value = int(self.request.GET.get("list"))
            set_list_value_in_cache(list_value)
            
            return list_value
        else:
            return get_list_value_from_cache() or self.paginate_by


    def get_queryset(self):
        # Aqui você pode adicionar filtros personalizados se necessário
        return Cliente.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtendo o perfil do usuário
        user_profiles = UserProfile.objects.filter(user=self.request.user)
        context['UserProfiles'] = user_profiles.first() if user_profiles.exists() else None
        
        # Adicionando informações personalizadas ao contexto
        context['model_name'] = 'Clientes'
        context['ActionAdd'] = ListAction(
            url_name='Cliente_create', label='Adicionar Cliente', icon='fa fa-plus', cor='w3-green'
        )
        context['list_actions'] = [
            ListAction(url_name='Cliente_edit', label='Atualizar', icon='fa fa-edit', cor='w3-blue'),
            ListAction(url_name='Cliente_delete', label='Excluir', icon='fa fa-trash', cor='w3-red'),
        ]
        context['column_titles'] = [f.name for f in Cliente._meta.fields]
        context['get_attribute'] = get_attribute
        return context

    # def get(self, request, *args, **kwargs):
    #     # Redireciona após ajustar o valor da lista
    #     if request.GET.get("list") and request.GET.get("list").isdigit():
    #         return redirect('Cliente_list')
    #     return super().get(request, *args, **kwargs)
    
class Cliente_create(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'generico/form_client.html'
    permission_required = 'produtos.add_cliente'
    raise_exception = True
    success_url = reverse_lazy('Cliente_list')

    # Sobrescreve o método form_valid para adicionar a mensagem de sucesso
    def form_valid(self, form):
        messages.success(self.request, "Cadastro realizado com sucesso!")
        return super().form_valid(form)

    # Sobrescreve o método form_invalid para adicionar a mensagem de erro
    def form_invalid(self, form):
        messages.warning(self.request, "Erro ao validar os dados, por favor preencha corretamente ou tente novamente mais tarde!")
        return super().form_invalid(form)

    # Adiciona variáveis de contexto extras (como 'ActionCancel' e 'model_name')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = 'Cadastro de Cliente'
        context['ActionCancel'] = reverse_lazy('Cliente_list')  # URL para cancelar a operação
        return context
    
class Cliente_edit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'generico/form_client.html'
    permission_required = 'produtos.change_cliente'
    raise_exception = True
    success_url = reverse_lazy('Cliente_list')

    def form_valid(self, form):
        messages.success(self.request, "Atualização realizada com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "Erro ao validar dados, por favor preencha corretamente ou tente novamente mais tarde!")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = 'Atualizar Cliente'
        context['ActionCancel'] = reverse_lazy('Cliente_list')
        return context

class Cliente_delete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'generico/form_delete_client.html'
    permission_required = 'produtos.delete_cliente'
    raise_exception = True
    success_url = reverse_lazy('Cliente_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = 'Deletar Cliente'
        context['ActionCancel'] = 'Cliente_list'
        return context