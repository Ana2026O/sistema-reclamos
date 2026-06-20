from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registrar/', views.registrar_reclamo, name='registrar_reclamo'),
]
