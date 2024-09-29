from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     
     path('', Cliente_list.as_view(), name='Cliente_list'),
     path('create', Cliente_create.as_view(), name='Cliente_create'),
     path('edit/<int:pk>', Cliente_edit.as_view(), name='Cliente_edit'),
     path('delete/<int:pk>', Cliente_delete.as_view(), name='Cliente_delete'),

     # path('api_request/', api_request_view, name='api_request'),
] 