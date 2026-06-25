from django.urls import path
from . import views

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
path('reclamos/editar/<int:reclamo_id>/', views.editar_reclamo, name='editar_reclamo'),

# Gestión de Categorías

path("categorias/", views.lista_categorias, name="categorias"),
path("categorias/editar/<int:pk>/", views.editar_categoria, name="editar_categoria"),
path("categorias/eliminar/<int:pk>/", views.eliminar_categoria, name="eliminar_categoria"),








]
