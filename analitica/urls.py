from django.urls import path
from . import views

urlpatterns = [
    path('loginEmpleo/', views.loginEmpleo, name='loginEmpleo'),
    path('loginEmpresa/', views.loginEmpresa, name='loginEmpresa'),
    path('', views.inicio, name='inicio')
]