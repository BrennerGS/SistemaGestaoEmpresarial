from django.urls import path
from django.conf.urls.static import static

from configuracao.views import configuracao_create, configuracao_delete, configuracao_edit, configuracao_list

urlpatterns = [
     
     path('', configuracao_list.as_view(), name='configuracao_sistema_list'),
     path('create', configuracao_create.as_view(), name='adicionar_configuracao_sistema'),
     path('edit/<int:pk>', configuracao_edit.as_view(), name='editar_configuracao_sistema'),
     path('delete/<int:pk>', configuracao_delete.as_view(), name='deletar_configuracao_sistema'),


     # path('api_request/', api_request_view, name='api_request'),
] 