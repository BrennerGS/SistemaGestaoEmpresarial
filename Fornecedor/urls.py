from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from Fornecedor.views import Fornecedor_create, Fornecedor_delete, Fornecedor_edit, Fornecedor_list


urlpatterns = [
     
     path('', Fornecedor_list.as_view(), name='Fornecedor_list'),
     path('create', Fornecedor_create.as_view(), name='Fornecedor_create'),
     path('edit/<int:pk>', Fornecedor_edit.as_view(), name='Fornecedor_edit'),
     path('delete/<int:pk>', Fornecedor_delete.as_view(), name='Fornecedor_delete'),

     # path('api_request/', api_request_view, name='api_request'),
] 