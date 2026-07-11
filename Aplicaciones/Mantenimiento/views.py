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
    nombres = request.POST.get('nombres_cond', '').strip()
    apellidos = request.POST.get('apell_cond', '').strip()
    cedula = request.POST.get('cedula_cond', '').strip()
    licencia = request.POST.get('tipolicen_cond', '').strip()
    telefono = request.POST.get('telfno_cond', '').strip()  # opcional

    # --- Validaciones obligatorias ---
    if not nombres or not apellidos or not cedula or not licencia:
        messages.error(request, 'Nombres, apellidos, cédula y licencia son obligatorios.')
        return redirect('/Conductor/nuevoConductor/')

    if not cedula.isdigit() or len(cedula) != 10:
        messages.error(request, 'La cédula debe tener 10 dígitos numéricos.')
        return redirect('/Conductor/nuevoConductor/')

    if Conductor.objects.filter(cedula_cond=cedula).exists():
        messages.error(request, 'Ya existe un conductor registrado con esa cédula.')
        return redirect('/Conductor/nuevoConductor/')

    # --- Validación opcional (solo si se llenó) ---
    if telefono and (not telefono.isdigit() or len(telefono) not in (7, 10)):
        messages.error(request, 'El teléfono debe ser numérico (7 o 10 dígitos).')
        return redirect('/Conductor/nuevoConductor/')

    Conductor.objects.create(
        nombres_cond=nombres,
        apell_cond=apellidos,
        cedula_cond=cedula,
        tipolicen_cond=licencia,
        telfno_cond=telefono or None
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
    conductor = get_object_or_404(Conductor, id=request.POST.get('id_cond'))

    nombres = request.POST.get('nombres_cond', '').strip()
    apellidos = request.POST.get('apell_cond', '').strip()
    cedula = request.POST.get('cedula_cond', '').strip()
    licencia = request.POST.get('tipolicen_cond', '').strip()
    telefono = request.POST.get('telfno_cond', '').strip()  # opcional

    if not nombres or not apellidos or not cedula or not licencia:
        messages.error(request, 'Nombres, apellidos, cédula y licencia son obligatorios.')
        return redirect('/Conductor/nuevoConductor/')

    if not cedula.isdigit() or len(cedula) != 10:
        messages.error(request, 'La cédula debe tener 10 dígitos numéricos.')
        return redirect('/Conductor/nuevoConductor/')

    if Conductor.objects.filter(cedula_cond=cedula).exclude(id=conductor.id).exists():
        messages.error(request, 'Ya existe otro conductor con esa cédula.')
        return redirect('/Conductor/nuevoConductor/')

    if telefono and (not telefono.isdigit() or len(telefono) not in (7, 10)):
        messages.error(request, 'El teléfono debe ser numérico (7 o 10 dígitos).')
        return redirect('/Conductor/nuevoConductor/')

    conductor.nombres_cond = nombres
    conductor.apell_cond = apellidos
    conductor.cedula_cond = cedula
    conductor.tipolicen_cond = licencia
    conductor.telfno_cond = telefono or None
    conductor.save()
    messages.success(request, 'Conductor actualizado correctamente.')
    return redirect('/Conductor/nuevoConductor/')

@login_required
@rol_requerido(['admin', 'superadmin'])
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
    nombre = request.POST.get('nombre_marca', '').strip()

    if not nombre or len(nombre) < 2:
        messages.error(request, 'El nombre de la marca debe tener al menos 2 caracteres.')
        return redirect('/Marca/')

    if Marca.objects.filter(nombre_marca__iexact=nombre).exists():
        messages.error(request, f'Ya existe la marca {nombre}.')
        return redirect('/Marca/')

    Marca.objects.create(nombre_marca=nombre)
    messages.success(request, 'Marca registrada correctamente.')
    return redirect('/Marca/')


@login_required
@rol_requerido(['admin', 'superadmin'])
def procesarEdicionMarca(request):
    marca = get_object_or_404(Marca, id=request.POST.get('id_marca'))
    nombre = request.POST.get('nombre_marca', '').strip()

    if not nombre or len(nombre) < 2:
        messages.error(request, 'El nombre de la marca debe tener al menos 2 caracteres.')
        return redirect('/Marca/')

    if Marca.objects.filter(nombre_marca__iexact=nombre).exclude(id=marca.id).exists():
        messages.error(request, f'Ya existe otra marca con el nombre {nombre}.')
        return redirect('/Marca/')

    marca.nombre_marca = nombre
    marca.save()
    messages.success(request, 'Marca actualizada correctamente.')
    return redirect('/Marca/')


@login_required
@rol_requerido(['admin', 'superadmin'])
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
    placa = request.POST.get('placa', '').strip().upper()
    marca_id = request.POST.get('marca_id', '').strip()
    anio = request.POST.get('anio', '').strip()
    estado = request.POST.get('estado', '').strip()
    num_motor = request.POST.get('num_motor', '').strip() or None
    num_chasis = request.POST.get('num_chasis', '').strip() or None

    # --- Obligatorios ---
    if not placa or not marca_id or not anio or not estado:
        messages.error(request, 'Placa, marca, año y estado son obligatorios.')
        return redirect('/Cabezal/')

    if not anio.isdigit() or not (1980 <= int(anio) <= 2100):
        messages.error(request, 'El año debe ser un número válido entre 1980 y 2100.')
        return redirect('/Cabezal/')

    if Activo.objects.filter(placa=placa).exists():
        messages.error(request, f'Ya existe un cabezal con la placa {placa}.')
        return redirect('/Cabezal/')

    if num_motor and Activo.objects.filter(num_motor=num_motor).exists():
        messages.error(request, f'Ya existe un cabezal con el número de motor {num_motor}.')
        return redirect('/Cabezal/')

    if num_chasis and Activo.objects.filter(num_chasis=num_chasis).exists():
        messages.error(request, f'Ya existe un cabezal con el número de chasis {num_chasis}.')
        return redirect('/Cabezal/')

    Activo.objects.create(
        placa=placa,
        marca_id=marca_id,
        modelo=request.POST.get('modelo', '').strip() or None,
        anio=anio,
        num_motor=num_motor,
        num_chasis=num_chasis,
        num_disco=request.POST.get('num_disco', '').strip() or None,
        color=request.POST.get('color', '').strip() or None,
        estado=estado,
        fecha_caducidad=request.POST.get('fecha_caducidad') or None,
    )
    messages.success(request, 'Cabezal registrado correctamente.')
    return redirect('/Cabezal/')


@login_required
@rol_requerido(['admin', 'superadmin'])
def procesarEdicionCabezal(request):
    cabezal = get_object_or_404(Activo, id=request.POST.get('id_cabezal'))

    placa = request.POST.get('placa', '').strip().upper()
    marca_id = request.POST.get('marca_id', '').strip()
    anio = request.POST.get('anio', '').strip()
    estado = request.POST.get('estado', '').strip()
    num_motor = request.POST.get('num_motor', '').strip() or None
    num_chasis = request.POST.get('num_chasis', '').strip() or None

    if not placa or not marca_id or not anio or not estado:
        messages.error(request, 'Placa, marca, año y estado son obligatorios.')
        return redirect('/Cabezal/')

    if not anio.isdigit() or not (1980 <= int(anio) <= 2100):
        messages.error(request, 'El año debe ser un número válido entre 1980 y 2100.')
        return redirect('/Cabezal/')

    if Activo.objects.filter(placa=placa).exclude(id=cabezal.id).exists():
        messages.error(request, f'Ya existe otro cabezal con la placa {placa}.')
        return redirect('/Cabezal/')

    if num_motor and Activo.objects.filter(num_motor=num_motor).exclude(id=cabezal.id).exists():
        messages.error(request, f'Ya existe otro cabezal con el número de motor {num_motor}.')
        return redirect('/Cabezal/')

    if num_chasis and Activo.objects.filter(num_chasis=num_chasis).exclude(id=cabezal.id).exists():
        messages.error(request, f'Ya existe otro cabezal con el número de chasis {num_chasis}.')
        return redirect('/Cabezal/')

    cabezal.placa = placa
    cabezal.marca_id = marca_id
    cabezal.modelo = request.POST.get('modelo', '').strip() or None
    cabezal.anio = anio
    cabezal.num_motor = num_motor
    cabezal.num_chasis = num_chasis
    cabezal.num_disco = request.POST.get('num_disco', '').strip() or None
    cabezal.color = request.POST.get('color', '').strip() or None
    cabezal.estado = estado
    cabezal.fecha_caducidad = request.POST.get('fecha_caducidad') or None
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
    nombre = request.POST.get('nombre', '').strip()
    tipo = request.POST.get('tipo', '').strip()
    marca_id = request.POST.get('marca_id', '').strip()
    anio = request.POST.get('anio', '').strip()
    estado = request.POST.get('estado', '').strip()
    observaciones = request.POST.get('observaciones', '').strip()  # opcional

    # --- Obligatorios ---
    if not nombre or not tipo or not marca_id or not anio or not estado:
        messages.error(request, 'Nombre, tipo, marca, año y estado son obligatorios.')
        return redirect('/Remolque/')

    if not anio.isdigit() or not (1980 <= int(anio) <= 2100):
        messages.error(request, 'El año debe ser un número válido entre 1980 y 2100.')
        return redirect('/Remolque/')

    Remolque.objects.create(
        nombre=nombre,
        tipo=tipo,
        marca_id=marca_id,
        anio=anio,
        estado=estado,
        observaciones=observaciones or None
    )
    messages.success(request, 'Remolque registrado correctamente.')
    return redirect('/Remolque/')


@login_required
@rol_requerido(['admin', 'superadmin'])
def procesarEdicionRemolque(request):
    remolque = get_object_or_404(Remolque, id=request.POST.get('id_remolque'))

    nombre = request.POST.get('nombre', '').strip()
    tipo = request.POST.get('tipo', '').strip()
    marca_id = request.POST.get('marca_id', '').strip()
    anio = request.POST.get('anio', '').strip()
    estado = request.POST.get('estado', '').strip()
    observaciones = request.POST.get('observaciones', '').strip()  # opcional

    if not nombre or not tipo or not marca_id or not anio or not estado:
        messages.error(request, 'Nombre, tipo, marca, año y estado son obligatorios.')
        return redirect('/Remolque/')

    if not anio.isdigit() or not (1980 <= int(anio) <= 2100):
        messages.error(request, 'El año debe ser un número válido entre 1980 y 2100.')
        return redirect('/Remolque/')

    remolque.nombre = nombre
    remolque.tipo = tipo
    remolque.marca_id = marca_id
    remolque.anio = anio
    remolque.estado = estado
    remolque.observaciones = observaciones or None
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
    nombre = request.POST.get('nombre', '').strip()
    aplica_a = request.POST.get('aplica_a', '').strip()
    tipo_control = request.POST.get('tipo_control', '').strip()
    descripcion = request.POST.get('descripcion', '').strip()  # opcional

    # --- Obligatorios ---
    if not nombre or len(nombre) < 2:
        messages.error(request, 'El nombre debe tener al menos 2 caracteres.')
        return redirect('/TipoTrabajo/')

    if not aplica_a or not tipo_control:
        messages.error(request, 'Debe indicar a qué aplica y el tipo de control.')
        return redirect('/TipoTrabajo/')

    if TipoTrabajo.objects.filter(nombre__iexact=nombre).exists():
        messages.error(request, f'Ya existe el trabajo {nombre}.')
        return redirect('/TipoTrabajo/')

    TipoTrabajo.objects.create(
        nombre=nombre,
        descripcion=descripcion or None,
        aplica_a=aplica_a,
        tipo_control=tipo_control
    )
    messages.success(request, 'Tipo de trabajo registrado correctamente.')
    return redirect('/TipoTrabajo/')


@login_required
@rol_requerido(['admin', 'superadmin'])
def procesarEdicionTipoTrabajo(request):
    trabajo = get_object_or_404(TipoTrabajo, id=request.POST.get('id_trabajo'))

    nombre = request.POST.get('nombre', '').strip()
    aplica_a = request.POST.get('aplica_a', '').strip()
    tipo_control = request.POST.get('tipo_control', '').strip()
    descripcion = request.POST.get('descripcion', '').strip()  # opcional

    if not nombre or len(nombre) < 2:
        messages.error(request, 'El nombre debe tener al menos 2 caracteres.')
        return redirect('/TipoTrabajo/')

    if not aplica_a or not tipo_control:
        messages.error(request, 'Debe indicar a qué aplica y el tipo de control.')
        return redirect('/TipoTrabajo/')

    if TipoTrabajo.objects.filter(nombre__iexact=nombre).exclude(id=trabajo.id).exists():
        messages.error(request, f'Ya existe otro trabajo con el nombre {nombre}.')
        return redirect('/TipoTrabajo/')

    trabajo.nombre = nombre
    trabajo.descripcion = descripcion or None
    trabajo.aplica_a = aplica_a
    trabajo.tipo_control = tipo_control
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
    marca_id = request.POST.get('marca_id', '').strip()
    trabajo_id = request.POST.get('trabajo_id', '').strip()
    km_intervalo = request.POST.get('km_intervalo', '').strip()

    # --- Todos obligatorios ---
    if not marca_id or not trabajo_id or not km_intervalo:
        messages.error(request, 'Marca, trabajo e intervalo en km son obligatorios.')
        return redirect('/ConfiguracionMan/')

    if not km_intervalo.isdigit() or int(km_intervalo) <= 0:
        messages.error(request, 'El intervalo en km debe ser un número entero mayor a 0.')
        return redirect('/ConfiguracionMan/')

    if ConfiguracionMantenimiento.objects.filter(marca_id=marca_id, trabajo_id=trabajo_id).exists():
        messages.error(request, 'Ya existe una configuración para esa marca y trabajo.')
        return redirect('/ConfiguracionMan/')

    ConfiguracionMantenimiento.objects.create(
        marca_id=marca_id,
        trabajo_id=trabajo_id,
        km_intervalo=km_intervalo
    )
    messages.success(request, 'Configuración registrada correctamente.')
    return redirect('/ConfiguracionMan/')


@login_required
@rol_requerido(['admin', 'superadmin'])
def procesarEdicionConfiguracion(request):
    config = get_object_or_404(ConfiguracionMantenimiento, id=request.POST.get('id_config'))

    marca_id = request.POST.get('marca_id', '').strip()
    trabajo_id = request.POST.get('trabajo_id', '').strip()
    km_intervalo = request.POST.get('km_intervalo', '').strip()

    if not marca_id or not trabajo_id or not km_intervalo:
        messages.error(request, 'Marca, trabajo e intervalo en km son obligatorios.')
        return redirect('/ConfiguracionMan/')

    if not km_intervalo.isdigit() or int(km_intervalo) <= 0:
        messages.error(request, 'El intervalo en km debe ser un número entero mayor a 0.')
        return redirect('/ConfiguracionMan/')

    if ConfiguracionMantenimiento.objects.filter(
        marca_id=marca_id, trabajo_id=trabajo_id
    ).exclude(id=config.id).exists():
        messages.error(request, 'Ya existe otra configuración para esa marca y trabajo.')
        return redirect('/ConfiguracionMan/')

    config.marca_id = marca_id
    config.trabajo_id = trabajo_id
    config.km_intervalo = km_intervalo
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
    from .models import DetalleMantenimiento, ConfiguracionMantenimiento

    activo_id = request.POST.get('activo_id') or None
    remolque_id = request.POST.get('remolque_id') or None
    cabezal_ref_id = request.POST.get('cabezal_ref_id') or None
    conductor_id = request.POST.get('conductor_id') or None
    tipo = request.POST.get('tipo', '').strip()
    fecha_entrada = request.POST.get('fecha_entrada', '').strip()
    km_odometro = request.POST.get('km_odometro') or None
    costo_total = request.POST.get('costo_total') or None
    fecha_pago = request.POST.get('fecha_pago') or None
    fecha_salida = request.POST.get('fecha_salida') or None
    observaciones = request.POST.get('observaciones', '').strip() or None

    trabajos = request.POST.getlist('trabajo_id[]')
    observaciones_trabajos = request.POST.getlist('trabajo_observacion[]')

    # --- Obligatorios ---
    if not activo_id and not remolque_id:
        messages.error(request, 'Debe seleccionar un cabezal o un remolque.')
        return redirect('/Mantenimiento/')

    if activo_id and remolque_id:
        messages.error(request, 'Solo puede seleccionar cabezal O remolque, no ambos.')
        return redirect('/Mantenimiento/')

    if not conductor_id or not tipo or not fecha_entrada:
        messages.error(request, 'Conductor, tipo y fecha de entrada son obligatorios.')
        return redirect('/Mantenimiento/')

    if activo_id and not km_odometro:
        messages.error(request, 'El km del odómetro es obligatorio para cabezales.')
        return redirect('/Mantenimiento/')

    if km_odometro is not None and (not str(km_odometro).isdigit() or int(km_odometro) < 0):
        messages.error(request, 'El km del odómetro debe ser un número válido.')
        return redirect('/Mantenimiento/')

    if not any(trabajos):
        messages.error(request, 'Debe agregar al menos un trabajo realizado.')
        return redirect('/Mantenimiento/')

    # --- Validar que los trabajos existan antes de crear el mantenimiento ---
    trabajos_validos = []
    for i, trabajo_id in enumerate(trabajos):
        if not trabajo_id:
            continue
        try:
            trabajo = TipoTrabajo.objects.get(id=trabajo_id)
        except TipoTrabajo.DoesNotExist:
            messages.error(request, 'Uno de los trabajos seleccionados no es válido.')
            return redirect('/Mantenimiento/')
        obs = observaciones_trabajos[i].strip() if i < len(observaciones_trabajos) else ''
        trabajos_validos.append((trabajo, obs or None))

    mant = Mantenimiento.objects.create(
        activo_id=activo_id,
        remolque_id=remolque_id,
        cabezal_ref_id=cabezal_ref_id,
        conductor_id=conductor_id,
        tipo=tipo,
        fecha_entrada=fecha_entrada,
        fecha_salida=fecha_salida,
        km_odometro=km_odometro,
        costo_total=costo_total,
        fecha_pago=fecha_pago,
        observaciones=observaciones
    )

    for trabajo, obs in trabajos_validos:
        config = None
        if trabajo.tipo_control == 'km' and activo_id:
            config = ConfiguracionMantenimiento.objects.filter(
                marca_id=Activo.objects.get(id=activo_id).marca_id,
                trabajo_id=trabajo.id
            ).first()
        DetalleMantenimiento.objects.create(
            mantenimiento=mant,
            trabajo=trabajo,
            config=config,
            observacion=obs or ''
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
    activo_id = request.POST.get('activo_id', '').strip()
    fecha = request.POST.get('fecha', '').strip()
    km_odometro = request.POST.get('km_odometro', '').strip()
    litros = request.POST.get('litros', '').strip()
    costo_total = request.POST.get('costo_total', '').strip()
    observaciones = request.POST.get('observaciones', '').strip()  # opcional

    # --- Obligatorios ---
    if not activo_id or not fecha or not km_odometro or not litros or not costo_total:
        messages.error(request, 'Cabezal, fecha, km odómetro, litros y costo total son obligatorios.')
        return redirect('/Combustible/')

    try:
        km_val = float(km_odometro)
        litros_val = float(litros)
        costo_val = float(costo_total)
    except ValueError:
        messages.error(request, 'Km odómetro, litros y costo deben ser numéricos.')
        return redirect('/Combustible/')

    if km_val < 0:
        messages.error(request, 'El km del odómetro no puede ser negativo.')
        return redirect('/Combustible/')

    if litros_val <= 0:
        messages.error(request, 'Los litros deben ser mayores a 0.')
        return redirect('/Combustible/')

    if costo_val <= 0:
        messages.error(request, 'El costo total debe ser mayor a 0.')
        return redirect('/Combustible/')

    if not Activo.objects.filter(id=activo_id).exists():
        messages.error(request, 'El cabezal seleccionado no es válido.')
        return redirect('/Combustible/')

    CargaCombustible.objects.create(
        activo_id=activo_id,
        registrado_por=request.user,
        fecha=fecha,
        km_odometro=km_val,
        litros=litros_val,
        costo_total=costo_val,
        observaciones=observaciones or None
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
    detalle_id = request.POST.get('detalle_id', '').strip()
    nombre_insumo = request.POST.get('nombre_insumo', '').strip()
    cantidad = request.POST.get('cantidad', '').strip()
    unidad = request.POST.get('unidad', '').strip()
    costo_unitario = request.POST.get('costo_unitario', '').strip() or None
    mantenimiento_id = request.POST.get('mantenimiento_id', '').strip()

    if not detalle_id or not nombre_insumo or not cantidad or not unidad:
        messages.error(request, 'Detalle, nombre del insumo, cantidad y unidad son obligatorios.')
        return redirect(f'/Mantenimiento/detalle/{mantenimiento_id}/')

    try:
        cantidad_val = float(cantidad)
        if cantidad_val <= 0:
            raise ValueError
    except ValueError:
        messages.error(request, 'La cantidad debe ser un número mayor a 0.')
        return redirect(f'/Mantenimiento/detalle/{mantenimiento_id}/')

    if costo_unitario:
        try:
            costo_unitario = float(costo_unitario)
            if costo_unitario < 0:
                raise ValueError
        except ValueError:
            messages.error(request, 'El costo unitario debe ser un número válido.')
            return redirect(f'/Mantenimiento/detalle/{mantenimiento_id}/')

    InsumoDetalle.objects.create(
        detalle_id=detalle_id,
        nombre_insumo=nombre_insumo,
        cantidad=cantidad_val,
        unidad=unidad,
        costo_unitario=costo_unitario
    )
    messages.success(request, 'Insumo agregado correctamente.')
    return redirect(f'/Mantenimiento/detalle/{mantenimiento_id}/')


@login_required
@rol_requerido(['admin', 'superadmin'])
def eliminarInsumo(request, id_insumo):
    insumo = get_object_or_404(InsumoDetalle, id=id_insumo)
    mantenimiento_id = insumo.detalle.mantenimiento.id
    insumo.delete()
    messages.success(request, 'Insumo eliminado.')
    return redirect(f'/Mantenimiento/detalle/{mantenimiento_id}/')