from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    path(
        'registrar/',
        views.registrar_reclamo,
        name='registrar_reclamo'
    ),

    path(
        'confirmacion/',
        views.confirmacion_reclamo,
        name='confirmacion_reclamo'
    ),

    path(
        'consulta/',
        views.consulta_reclamo,
        name='consulta_reclamo'
    ),

    path(
        'login/',
        views.login_admin,
        name='login_admin'
    ),

    path(
        'menu-admin/',
        views.menu_admin,
        name='menu_admin'
    ),

    path(
        'alta-usuario/',
        views.alta_usuario,
        name='alta_usuario'
    ),

    path(
        'panel/',
        views.panel_control,
        name='panel_control'
    ),

path(
    'detalle/<int:id>/',
    views.detalle_reclamo,
    name='detalle_reclamo'
),  




]