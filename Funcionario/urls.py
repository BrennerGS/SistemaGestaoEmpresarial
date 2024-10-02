from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from Funcionario.views import Funcionario_create, Funcionario_delete, Funcionario_edit, Funcionario_list

urlpatterns = [
     
     path('', Funcionario_list.as_view(), name='Funcionario_list'),
     path('create', Funcionario_create.as_view(), name='Funcionario_create'),
     path('edit/<int:pk>', Funcionario_edit.as_view(), name='Funcionario_edit'),
     path('delete/<int:pk>', Funcionario_delete.as_view(), name='Funcionario_delete'),

     # path('api_request/', api_request_view, name='api_request'),
] 