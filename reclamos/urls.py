from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),   # <- esta línea falta
    path('', include('reclamos.urls')),  # tus rutas de la app
]

from .views import lista_usuarios, alta_usuario, eliminar_usuario





urlpatterns = [
    path('', views.inicio, name='inicio'),

    path('registrar/', views.registrar_reclamo, name='registrar_reclamo'),

    path('confirmacion/<int:reclamo_id>/', views.confirmacion_reclamo, name='confirmacion_reclamo'),

    path('consulta/', views.consulta_reclamo, name='consulta_reclamo'),

    path('login/', views.login_admin, name='login_admin'),


    path('menu-admin/', views.menu_admin, name='menu_admin'),

   

    path('detalle/<int:reclamo_id>/', views.detalle_reclamo, name='detalle_reclamo'),

    path('pdf/<int:reclamo_id>/', views.descargar_pdf, name='descargar_pdf'),  


    path('alta_usuario/', views.alta_usuario, name='alta_usuario'),
    path('panel_control/', views.panel_control, name='panel_control'),
    path('reportes/', views.reportes, name='reportes'),
    
    
    
path('reclamos/eliminar/<int:reclamo_id>/', views.eliminar_reclamo, name='eliminar_reclamo'),


# Gestión de Categorías

path("categorias/", views.lista_categorias, name="categorias"),
path("categorias/editar/<int:pk>/", views.editar_categoria, name="editar_categoria"),
path("categorias/eliminar/<int:pk>/", views.eliminar_categoria, name="eliminar_categoria"),



 path('usuarios/', lista_usuarios, name='lista_usuarios'),
    path('usuarios/nuevo/', alta_usuario, name='alta_usuario'),
    path('usuarios/<int:pk>/modificar/', alta_usuario, name='modificar_usuario'),
    path('usuarios/<int:pk>/eliminar/', eliminar_usuario, name='eliminar_usuario'),

    
  path('estadisticas/', views.estadisticas_reclamos, name='reportes'),
    path('reclamos/pdf/', views.reclamos_pdf, name='reclamos_pdf'),




path("reclamos/editar/<int:pk>/", views.editar_reclamo, name="editar_reclamo")

]



