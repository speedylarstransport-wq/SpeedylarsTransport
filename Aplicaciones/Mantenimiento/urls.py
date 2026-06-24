from django.urls import path
from . import views
urlpatterns = [
   # Conductores
    path('Conductor/', views.listadoConductor, name='listadoConductor'),
    path('Conductor/nuevoConductor/', views.nuevoConductor, name='nuevoConductor'),
    path('Conductor/guardar/', views.guardarConductor, name='guardarConductor'),
    path('Conductor/editar/<int:id_cond>/', views.editarConductor, name='editarConductor'),
    path('Conductor/procesarEdicionConductor/', views.procesarEdicionConductor, name='procesarEdicionConductor'),
    path('Conductor/eliminar/<int:id_cond>/', views.eliminarConductor, name='eliminarConductor'),
    
    # Marca
    path('Marca/', views.gestionMarca, name='gestionMarca'),
    path('Marca/guardar/', views.guardarMarca, name='guardarMarca'),
    path('Marca/procesarEdicion/', views.procesarEdicionMarca, name='procesarEdicionMarca'),
    path('Marca/eliminar/<int:id_marca>/', views.eliminarMarca, name='eliminarMarca'),
    
    # Cabezales
    path('Cabezal/', views.gestionCabezal, name='gestionCabezal'),
    path('Cabezal/guardar/', views.guardarCabezal, name='guardarCabezal'),
    path('Cabezal/procesarEdicion/', views.procesarEdicionCabezal, name='procesarEdicionCabezal'),
    path('Cabezal/eliminar/<int:id_cabezal>/', views.eliminarCabezal, name='eliminarCabezal'),
    
    #Remolque
    path('Remolque/', views.gestionRemolque, name='gestionRemolque'),
    path('Remolque/guardar/', views.guardarRemolque, name='guardarRemolque'),
    path('Remolque/procesarEdicion/', views.procesarEdicionRemolque, name='procesarEdicionRemolque'),
    path('Remolque/eliminar/<int:id_remolque>/', views.eliminarRemolque, name='eliminarRemolque'),
    
    # Tipo de Trabajo
    path('TipoTrabajo/', views.gestionTipoTrabajo, name='gestionTipoTrabajo'),
    path('TipoTrabajo/guardar/', views.guardarTipoTrabajo, name='guardarTipoTrabajo'),
    path('TipoTrabajo/procesarEdicion/', views.procesarEdicionTipoTrabajo, name='procesarEdicionTipoTrabajo'),
    path('TipoTrabajo/eliminar/<int:id_trabajo>/', views.eliminarTipoTrabajo, name='eliminarTipoTrabajo'),
    
    # Configuracion
    path('ConfiguracionMan/', views.gestionConfiguracion, name='gestionConfiguracion'),
    path('ConfiguracionMan/guardar/', views.guardarConfiguracion, name='guardarConfiguracion'),
    path('ConfiguracionMan/procesarEdicion/', views.procesarEdicionConfiguracion, name='procesarEdicionConfiguracion'),
    path('ConfiguracionMan/eliminar/<int:id_config>/', views.eliminarConfiguracion, name='eliminarConfiguracion'),
    
    # Mantenimiento
    path('Mantenimiento/', views.gestionMantenimiento, name='gestionMantenimiento'),
    path('Mantenimiento/guardar/', views.guardarMantenimiento, name='guardarMantenimiento'),
    path('Mantenimiento/eliminar/<int:id_mant>/', views.eliminarMantenimiento, name='eliminarMantenimiento'),
    path('Mantenimiento/detalle/<int:id_mant>/', views.detalleMantenimiento, name='detalleMantenimiento'),
    
    path('Mantenimiento/insumo/guardar/', views.guardarInsumo, name='guardarInsumo'),
    path('Mantenimiento/insumo/eliminar/<int:id_insumo>/', views.eliminarInsumo, name='eliminarInsumo'),
    # Combustible
    path('Combustible/', views.gestionCombustible, name='gestionCombustible'),
    path('Combustible/guardar/', views.guardarCombustible, name='guardarCombustible'),
    path('Combustible/eliminar/<int:id_carga>/', views.eliminarCombustible, name='eliminarCombustible'),
    
   
]
