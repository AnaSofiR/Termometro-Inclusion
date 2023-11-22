from django.urls import path
from . import views

urlpatterns = [
    path('loginEmpleo/', views.loginEmpleo, name='loginEmpleo'),
    path('loginEmpresa/', views.loginEmpresa, name='loginEmpresa'),
    path('', views.inicio, name='inicio'),
    path('inicioEmpleo/', views.inicioEmpleo, name='inicioEmpleo'),
    path('ofertaRating/<int:offer_id>/', views.ofertaRating, name='ofertaRating'),
    path('rating/<int:offer_id>/<int:rating>/', views.rating),
    path('empleos/', views.empleos, name='empleos'),
    path('analisisEmpresa/<int:id_empresa>', views.analisisEmpresa, name='analisisEmpresa'),
]