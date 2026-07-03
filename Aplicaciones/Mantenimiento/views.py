from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Conductor, Marca, Activo, Remolque, TipoTrabajo, ConfiguracionMantenimiento, Mantenimiento, CargaCombustible, InsumoDetalle, DetalleMantenimiento
from django.contrib.auth.decorators import login_required
from Aplicaciones.PaginaW.decorators import rol_requerido

# Create your views here.
# =============================================
# CONDUCTORES
# =============================================

@login_required
@rol_requerido(['admin', 'superadmin'])
def listadoConductor(request):
    conductores = Conductor.objects.all()
    return render(request, 'Conductor/listadoConductor.html', {'conductores': conductores})

@login_required
@rol_requerido(['admin', 'superadmin'])
def nuevoConductor(request):
    conductores = Conductor.objects.all()
    return render(request, 'Conductor/nuevoConductor.html', {'conductores': conductores})
   
@login_required
@rol_requerido(['admin', 'superadmin'])
def guardarConductor(request):
    nombres = request.POST['nombres_cond']
    apellidos = request.POST['apell_cond']
    cedula = request.POST['cedula_cond']
    licencia = request.POST['tipolicen_cond']
    telefono = request.POST['telfno_cond']

    Conductor.objects.create(
        nombres_cond=nombres,
        apell_cond=apellidos,
        cedula_cond=cedula,
        tipolicen_cond=licencia,
        telfno_cond=telefono
    )
    messages.success(request, 'Conductor registrado correctamente.')
    return redirect('/Conductor/')


@login_required
@rol_requerido(['admin', 'superadmin'])
def editarConductor(request, id_cond):
    conductor = Conductor.objects.get(id_cond=id_cond)
    return render(request, 'Conductor/nuevoConductor.html', {'conductor': conductor})


@login_required
@rol_requerido(['admin', 'superadmin'])
def procesarEdicionConductor(request):
    conductor = Conductor.objects.get(id=request.POST['id_cond'])
    conductor.nombres_cond = request.POST['nombres_cond']
    conductor.apell_cond = request.POST['apell_cond']
    conductor.cedula_cond = request.POST['cedula_cond']
    conductor.tipolicen_cond = request.POST['tipolicen_cond']
    conductor.telfno_cond = request.POST['telfno_cond']
    conductor.save()
    messages.success(request, 'Conductor actualizado correctamente.')
    return redirect('/Conductor/nuevoConductor/')

def eliminarConductor(request, id_cond):
    conductor = get_object_or_404(Conductor, id=id_cond)
    conductor.delete()
    messages.success(request, 'Conductor eliminado.')
    return redirect('/Conductor/nuevoConductor/')

# =============================================
# MARCA
# =============================================
@login_required
@rol_requerido(['admin', 'superadmin'])
def gestionMarca(request):
    marcas = Marca.objects.all()
    return render(request, 'Marca/gestionMarca.html', {'marcas': marcas})


@login_required
@rol_requerido(['admin', 'superadmin'])
def guardarMarca(request):
    nombre = request.POST['nombre_marca']

    if Marca.objects.filter(nombre_marca=nombre).exists():
        messages.error(request, f'Ya existe la marca {nombre}.')
        return redirect('/Marca/')

    Marca.objects.create(nombre_marca=nombre)
    messages.success(request, 'Marca registrada correctamente.')
    return redirect('/Marca/')


@login_required
@rol_requerido(['admin', 'superadmin'])
def procesarEdicionMarca(request):
    marca = Marca.objects.get(id=request.POST['id_marca'])
    marca.nombre_marca = request.POST['nombre_marca']
    marca.save()
    messages.success(request, 'Marca actualizada correctamente.')
    return redirect('/Marca/')

def eliminarMarca(request, id_marca):
    marca = get_object_or_404(Marca, id=id_marca)
    marca.delete()
    messages.success(request, 'Marca eliminada.')
    return redirect('/Marca/')

# =============================================
# CABEZALES
# =============================================


@login_required
@rol_requerido(['admin', 'superadmin'])
def gestionCabezal(request):
    cabezales = Activo.objects.all()
    marcas = Marca.objects.all()
    return render(request, 'Cabezal/gestionCabezal.html', {
        'cabezales': cabezales,
        'marcas': marcas
    })

@login_required
@rol_requerido(['admin', 'superadmin'])
def guardarCabezal(request):
    placa = request.POST['placa']

    if Activo.objects.filter(placa=placa).exists():
        messages.error(request, f'Ya existe un cabezal con la placa {placa}.')
        return redirect('/Cabezal/')

    Activo.objects.create(
        placa=placa,
        marca_id=request.POST['marca_id'],
        modelo=request.POST['modelo'],
        anio=request.POST['anio'],
        num_motor=request.POST['num_motor'],
        num_chasis=request.POST['num_chasis'],
        num_disco=request.POST['num_disco'],
        color=request.POST['color'],
        estado=request.POST['estado'],
        fecha_caducidad=request.POST['fecha_caducidad'] or None,
    )
    messages.success(request, 'Cabezal registrado correctamente.')
    return redirect('/Cabezal/')

@login_required
@rol_requerido(['admin', 'superadmin'])
def procesarEdicionCabezal(request):
    cabezal = Activo.objects.get(id=request.POST['id_cabezal'])
    cabezal.placa = request.POST['placa']
    cabezal.marca_id = request.POST['marca_id']
    cabezal.modelo = request.POST['modelo']
    cabezal.anio = request.POST['anio']
    cabezal.num_motor = request.POST['num_motor']
    cabezal.num_chasis = request.POST['num_chasis']
    cabezal.num_disco = request.POST['num_disco']
    cabezal.color = request.POST['color']
    cabezal.estado = request.POST['estado']
    cabezal.fecha_caducidad = request.POST['fecha_caducidad'] or None
    cabezal.save()
    messages.success(request, 'Cabezal actualizado correctamente.')
    return redirect('/Cabezal/')


@login_required
@rol_requerido(['admin', 'superadmin'])
def eliminarCabezal(request, id_cabezal):
    cabezal = get_object_or_404(Activo, id=id_cabezal)
    cabezal.delete()
    messages.success(request, 'Cabezal eliminado.')
    return redirect('/Cabezal/')

# =============================================
# REMOLQUES
# =============================================
@login_required
@rol_requerido(['admin', 'superadmin'])
def gestionRemolque(request):
    remolques = Remolque.objects.all()
    marcas = Marca.objects.all()
    return render(request, 'Remolque/gestionRemolque.html', {
        'remolques': remolques,
        'marcas': marcas
    })

@login_required
@rol_requerido(['admin', 'superadmin'])
def guardarRemolque(request):
    Remolque.objects.create(
        nombre=request.POST['nombre'],
        tipo=request.POST['tipo'],
        marca_id=request.POST['marca_id'] or None,
        anio=request.POST['anio'] or None,
        estado=request.POST['estado'],
        observaciones=request.POST['observaciones']
    )
    messages.success(request, 'Remolque registrado correctamente.')
    return redirect('/Remolque/')

@login_required
@rol_requerido(['admin', 'superadmin'])
def procesarEdicionRemolque(request):
    remolque = Remolque.objects.get(id=request.POST['id_remolque'])
    remolque.nombre = request.POST['nombre']
    remolque.tipo = request.POST['tipo']
    remolque.marca_id = request.POST['marca_id'] or None
    remolque.anio = request.POST['anio'] or None
    remolque.estado = request.POST['estado']
    remolque.observaciones = request.POST['observaciones']
    remolque.save()
    messages.success(request, 'Remolque actualizado correctamente.')
    return redirect('/Remolque/')


@login_required
@rol_requerido(['admin', 'superadmin'])
def eliminarRemolque(request, id_remolque):
    remolque = get_object_or_404(Remolque, id=id_remolque)
    remolque.delete()
    messages.success(request, 'Remolque eliminado.')
    return redirect('/Remolque/')

# =============================================
# TIPO DE TRABAJO
# =============================================

@login_required
@rol_requerido(['admin', 'superadmin'])
def gestionTipoTrabajo(request):
    trabajos = TipoTrabajo.objects.all()
    return render(request, 'TipoTrabajo/gestionTipoTrabajo.html', {'trabajos': trabajos})

@login_required
@rol_requerido(['admin', 'superadmin'])
def guardarTipoTrabajo(request):
    nombre = request.POST['nombre']

    if TipoTrabajo.objects.filter(nombre=nombre).exists():
        messages.error(request, f'Ya existe el trabajo {nombre}.')
        return redirect('/TipoTrabajo/')

    TipoTrabajo.objects.create(
        nombre=nombre,
        descripcion=request.POST['descripcion'],
        aplica_a=request.POST['aplica_a'],
        tipo_control=request.POST['tipo_control']
    )
    messages.success(request, 'Tipo de trabajo registrado correctamente.')
    return redirect('/TipoTrabajo/')

@login_required
@rol_requerido(['admin', 'superadmin'])
def procesarEdicionTipoTrabajo(request):
    trabajo = TipoTrabajo.objects.get(id=request.POST['id_trabajo'])
    trabajo.nombre = request.POST['nombre']
    trabajo.descripcion = request.POST['descripcion']
    trabajo.aplica_a = request.POST['aplica_a']
    trabajo.tipo_control = request.POST['tipo_control']
    trabajo.save()
    messages.success(request, 'Tipo de trabajo actualizado correctamente.')
    return redirect('/TipoTrabajo/')

@login_required
@rol_requerido(['admin', 'superadmin'])
def eliminarTipoTrabajo(request, id_trabajo):
    trabajo = get_object_or_404(TipoTrabajo, id=id_trabajo)
    trabajo.delete()
    messages.success(request, 'Tipo de trabajo eliminado.')
    return redirect('/TipoTrabajo/')

# =============================================
# CONFIGURACION DE MANTENIMIENTO
# =============================================

@login_required
@rol_requerido(['admin', 'superadmin'])
def gestionConfiguracion(request):
    configuraciones = ConfiguracionMantenimiento.objects.select_related('marca', 'trabajo').all()
    marcas = Marca.objects.all()
    trabajos = TipoTrabajo.objects.filter(tipo_control='km')  # solo los que tienen intervalo
    return render(request, 'ConfiguracionMan/gestionConfiguracion.html', {
        'configuraciones': configuraciones,
        'marcas': marcas,
        'trabajos': trabajos
    })

@login_required
@rol_requerido(['admin', 'superadmin'])
def guardarConfiguracion(request):
    marca_id = request.POST['marca_id']
    trabajo_id = request.POST['trabajo_id']

    if ConfiguracionMantenimiento.objects.filter(marca_id=marca_id, trabajo_id=trabajo_id).exists():
        messages.error(request, 'Ya existe una configuración para esa marca y trabajo.')
        return redirect('/ConfiguracionMan/')

    ConfiguracionMantenimiento.objects.create(
        marca_id=marca_id,
        trabajo_id=trabajo_id,
        km_intervalo=request.POST['km_intervalo']
    )
    messages.success(request, 'Configuración registrada correctamente.')
    return redirect('/ConfiguracionMan/')

@login_required
@rol_requerido(['admin', 'superadmin'])
def procesarEdicionConfiguracion(request):
    config = ConfiguracionMantenimiento.objects.get(id=request.POST['id_config'])
    config.marca_id = request.POST['marca_id']
    config.trabajo_id = request.POST['trabajo_id']
    config.km_intervalo = request.POST['km_intervalo']
    config.save()
    messages.success(request, 'Configuración actualizada correctamente.')
    return redirect('/ConfiguracionMan/')

@login_required
@rol_requerido(['admin', 'superadmin'])
def eliminarConfiguracion(request, id_config):
    config = get_object_or_404(ConfiguracionMantenimiento, id=id_config)
    config.delete()
    messages.success(request, 'Configuración eliminada.')
    return redirect('/ConfiguracionMan/')

# =============================================
# MANTENIMIENTO
# =============================================


@login_required
@rol_requerido(['admin', 'superadmin', 'conductor'])
def gestionMantenimiento(request):
    mantenimientos = Mantenimiento.objects.select_related(
        'activo', 'remolque', 'conductor'
    ).all().order_by('-fecha_entrada')
    cabezales = Activo.objects.filter(estado='activo')
    remolques = Remolque.objects.filter(estado='activo')
    conductores = Conductor.objects.all()
    tipos_trabajo = TipoTrabajo.objects.all()
    return render(request, 'Mantenimiento/gestionMantenimiento.html', {
        'mantenimientos': mantenimientos,
        'cabezales': cabezales,
        'remolques': remolques,
        'conductores': conductores,
        'tipos_trabajo': tipos_trabajo 
    })

@login_required
@rol_requerido(['admin', 'superadmin', 'conductor'])
def guardarMantenimiento(request):
    activo_id = request.POST.get('activo_id') or None
    remolque_id = request.POST.get('remolque_id') or None
    cabezal_ref_id = request.POST.get('cabezal_ref_id') or None

    mant = Mantenimiento.objects.create(
        activo_id=activo_id,
        remolque_id=remolque_id,
        cabezal_ref_id=cabezal_ref_id,
        conductor_id=request.POST.get('conductor_id') or None,
        tipo=request.POST['tipo'],
        fecha_entrada=request.POST['fecha_entrada'],
        fecha_salida=request.POST.get('fecha_salida') or None,
        km_odometro=request.POST.get('km_odometro') or None,
        costo_total=request.POST.get('costo_total') or None,
        fecha_pago=request.POST.get('fecha_pago') or None,
        observaciones=request.POST.get('observaciones')
    )

    # Guardar trabajos
    trabajos = request.POST.getlist('trabajo_id[]')
    observaciones_trabajos = request.POST.getlist('trabajo_observacion[]')

    for i, trabajo_id in enumerate(trabajos):
        if trabajo_id:
            from .models import DetalleMantenimiento, ConfiguracionMantenimiento
            trabajo = TipoTrabajo.objects.get(id=trabajo_id)
            config = None
            if trabajo.tipo_control == 'km' and activo_id:
                config = ConfiguracionMantenimiento.objects.filter(
                    marca_id=Activo.objects.get(id=activo_id).marca_id,
                    trabajo_id=trabajo_id
                ).first()
            DetalleMantenimiento.objects.create(
                mantenimiento=mant,
                trabajo_id=trabajo_id,
                config=config,
                observacion=observaciones_trabajos[i] if i < len(observaciones_trabajos) else ''
            )

    messages.success(request, 'Mantenimiento registrado correctamente.')
    return redirect('/Mantenimiento/')


@login_required
@rol_requerido(['admin', 'superadmin', 'conductor'])
def eliminarMantenimiento(request, id_mant):
    mant = get_object_or_404(Mantenimiento, id=id_mant)
    mant.delete()
    messages.success(request, 'Mantenimiento eliminado.')
    return redirect('/Mantenimiento/')


@login_required
@rol_requerido(['admin', 'superadmin', 'conductor'])
def detalleMantenimiento(request, id_mant):
    mant = get_object_or_404(Mantenimiento, id=id_mant)
    detalles = DetalleMantenimiento.objects.select_related('trabajo').filter(mantenimiento=mant)
    return render(request, 'Mantenimiento/detalleMantenimiento.html', {
        'mant': mant,
        'detalles': detalles,
    })
    
# =============================================
# CARGA DE COMBUSTIBLE
# =============================================

@login_required
@rol_requerido(['admin', 'superadmin'])
def gestionCombustible(request):
    cargas = CargaCombustible.objects.select_related('activo', 'registrado_por').all().order_by('-fecha')
    cabezales = Activo.objects.filter(estado='activo')
    return render(request, 'Combustible/gestionCombustible.html', {
        'cargas': cargas,
        'cabezales': cabezales
    })


@login_required
@rol_requerido(['admin', 'superadmin'])
def guardarCombustible(request):
    CargaCombustible.objects.create(
        activo_id=request.POST['activo_id'],
        registrado_por_id=request.user,  # temporal hasta que esté el login
        fecha=request.POST['fecha'],
        km_odometro=request.POST['km_odometro'],
        litros=request.POST['litros'],
        costo_total=request.POST['costo_total'],
        observaciones=request.POST.get('observaciones')
    )
    messages.success(request, 'Carga de combustible registrada correctamente.')
    return redirect('/Combustible/')

@login_required
@rol_requerido(['admin', 'superadmin'])
def eliminarCombustible(request, id_carga):
    carga = get_object_or_404(CargaCombustible, id=id_carga)
    carga.delete()
    messages.success(request, 'Registro eliminado.')
    return redirect('/Combustible/')

@login_required
@rol_requerido(['admin', 'superadmin'])
def guardarInsumo(request):
    InsumoDetalle.objects.create(
        detalle_id=request.POST['detalle_id'],
        nombre_insumo=request.POST['nombre_insumo'],
        cantidad=request.POST['cantidad'],
        unidad=request.POST['unidad'],
        costo_unitario=request.POST.get('costo_unitario') or None
    )
    messages.success(request, 'Insumo agregado correctamente.')
    return redirect(f'/Mantenimiento/detalle/{request.POST["mantenimiento_id"]}/')

@login_required
@rol_requerido(['admin', 'superadmin'])
def eliminarInsumo(request, id_insumo):
    insumo = get_object_or_404(InsumoDetalle, id=id_insumo)
    mantenimiento_id = insumo.detalle.mantenimiento.id
    insumo.delete()
    messages.success(request, 'Insumo eliminado.')
    return redirect(f'/Mantenimiento/detalle/{mantenimiento_id}/')