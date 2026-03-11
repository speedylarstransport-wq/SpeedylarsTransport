from django.urls import path
from . import views
from .views import login_view, logout_view

urlpatterns = [
    path("", views.inicio, name='inicio'),
    path('contacto/', views.inicio, name='contacto'),
    path('quienesomos/', views.quienesomos, name='quienesomos'),
    path('servicios/', views.servicios, name='servicios'),
    path('contactanos/', views.contactanos, name='contactanos'),
    path('plantilla-admin/', views.aplicaciones, name='plantilla_admin'),
    

    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('usuarios/editar/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),

    path('conductor/nuevo/', views.nuevo_conductor, name='nuevo_conductor'),
    path('conductor/', views.listado_conductor, name='listado_conductor'),
    path('conductor/editar/<int:id>/', views.editar_conductor, name='editar_conductor'),
    path('conductor/desactivar/<int:id>/', views.desactivar_conductor, name='desactivar_conductor'),
    path('conductor/activar/<int:id>/', views.activar_conductor, name='activar_conductor'),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('recuperar-contrasena/', views.recuperar_contrasena, name='recuperar_contrasena'),

]
