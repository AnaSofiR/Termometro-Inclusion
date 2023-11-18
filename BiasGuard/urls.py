"""
URL configuration for BiasGuard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from BiasGuard1 import views as biasguardViews

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('',biasguardViews.home),
    path('oferta/', biasguardViews.oferta, name='oferta'),
    path('revision/', biasguardViews.revision, name='revision'),
    path('analitica/', include('analitica.urls')),
    path('editar/<int:id_offer>/<str:palabras_genero>/<str:palabras_edad>/<str:palabras_discapacidad>/', biasguardViews.editar, name='editar'),
    path('', include('analitica.urls')),
    path('inicioEmpresa/', biasguardViews.inicioEmpresa, name='inicioEmpresa'),
    path('empleos/', biasguardViews.empleos, name='empleos')
]
