from django.db import models
from django.conf import settings
# Create your models here.

# =============================================
# MARCA
# =============================================
class Marca(models.Model):
    nombre_marca = models.CharField(max_length=200, unique=True)

    class Meta:
        db_table = 'Marca'
        
    def __str__(self):
        return self.nombre_marca


# =============================================
# CONDUCTOR
# =============================================
class Conductor(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    nombres_cond = models.CharField(max_length=150)
    apell_cond = models.CharField(max_length=150)
    cedula_cond = models.CharField(max_length=20, unique=True)
    tipolicen_cond = models.CharField(max_length=3)
    telfno_cond = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'Conductor'
        

    def __str__(self):
        return f'{self.nombres_cond} {self.apell_cond}'


# =============================================
# ACTIVO (solo cabezales)
# =============================================
class Activo(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('mantenimiento', 'En mantenimiento'),
        ('inactivo', 'Inactivo'),
    ]

    placa = models.CharField(max_length=8, unique=True)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    anio = models.IntegerField()
    num_motor = models.CharField(max_length=50, unique=True, blank=True, null=True)
    num_chasis = models.CharField(max_length=50, unique=True, blank=True, null=True)
    num_disco = models.CharField(max_length=10, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    km_manual = models.IntegerField(default=0)
    fecha_caducidad = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'Activo'
        

    def __str__(self):
        return f'{self.placa} - {self.marca}'

    @property
    def km_odometro_actual(self):
        km_manto = self.mantenimiento_set.aggregate(
            models.Max('km_odometro'))['km_odometro__max'] or 0
        km_combustible = self.cargacombustible_set.aggregate(
            models.Max('km_odometro'))['km_odometro__max'] or 0
        return max(km_manto, km_combustible, self.km_manual or 0)
    
    @property
    def km_proximo_mantenimiento(self):
        from django.db.models import Max
        from .models import ConfiguracionMantenimiento
        
        ultimo = self.mantenimiento_set.filter(
            tipo='preventivo',
            km_odometro__isnull=False
        ).order_by('-km_odometro').first()
        
        if not ultimo:
            return None
        
        config = ConfiguracionMantenimiento.objects.filter(
            marca=self.marca
        ).first()
        
        if not config:
            return None
        
        return ultimo.km_odometro + config.km_intervalo

    @property
    def km_faltantes(self):
        proximo = self.km_proximo_mantenimiento
        if not proximo:
            return None
        return proximo - self.km_odometro_actual

    @property
    def estado_mantenimiento(self):
        from .models import ConfiguracionMantenimiento
        faltantes = self.km_faltantes
        if faltantes is None:
            return 'sin_datos'
        
        config = ConfiguracionMantenimiento.objects.filter(marca=self.marca).first()
        if not config:
            return 'sin_datos'
        
        ciclo = config.km_intervalo
        if faltantes <= 0:
            return 'vencido'
        elif faltantes <= ciclo * 0.05:
            return 'urgente'
        elif faltantes <= ciclo * 0.20:
            return 'falta_poco'
        return 'al_dia'


# =============================================
# REMOLQUE (furgones y plataformas)
# =============================================
class Remolque(models.Model):
    TIPO_CHOICES = [
        ('furgon', 'Furgón'),
        ('plataforma', 'Plataforma'),
    ]
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('mantenimiento', 'En mantenimiento'),
        ('inactivo', 'Inactivo'),
    ]

    nombre = models.CharField(max_length=150)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, blank=True, null=True)
    anio = models.IntegerField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Remolque'
       

    def __str__(self):
        return f'{self.nombre} ({self.get_tipo_display()})'


# =============================================
# TIPO DE TRABAJO
# =============================================
class TipoTrabajo(models.Model):
    APLICA_CHOICES = [
        ('cabezal', 'Cabezal'),
        ('furgon', 'Furgón'),
        ('plataforma', 'Plataforma'),
        ('ambos', 'Todos'),
    ]
    CONTROL_CHOICES = [
        ('km', 'Por kilometraje'),
        ('libre', 'Libre'),
    ]

    nombre = models.CharField(max_length=250, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    aplica_a = models.CharField(max_length=10, choices=APLICA_CHOICES)
    tipo_control = models.CharField(max_length=5, choices=CONTROL_CHOICES)

    class Meta:
        db_table = 'TipoTrabajo'
        

    def __str__(self):
        return self.nombre


# =============================================
# CONFIGURACION DE MANTENIMIENTO
# =============================================
class ConfiguracionMantenimiento(models.Model):
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    trabajo = models.ForeignKey(TipoTrabajo, on_delete=models.PROTECT)
    km_intervalo = models.IntegerField()

    class Meta:
        db_table = 'ConfiguracionMantenimiento'
        unique_together = ('marca', 'trabajo')

    def __str__(self):
        return f'{self.marca} - {self.trabajo} cada {self.km_intervalo} km'


# =============================================
# MANTENIMIENTO
# =============================================
class Mantenimiento(models.Model):
    TIPO_CHOICES = [
        ('preventivo', 'Preventivo'),
        ('correctivo', 'Correctivo'),
    ]

    # Solo uno de los dos tendrá valor
    activo = models.ForeignKey(Activo, on_delete=models.CASCADE,
                               blank=True, null=True)
    remolque = models.ForeignKey(Remolque, on_delete=models.CASCADE,
                                 blank=True, null=True)
    # A qué cabezal estaba enganchado el remolque cuando se hizo el mantenimiento
    cabezal_ref = models.ForeignKey(Activo, on_delete=models.SET_NULL,
                                    blank=True, null=True,
                                    related_name='mantenimientos_como_ref')
    conductor = models.ForeignKey(Conductor, on_delete=models.SET_NULL,
                                  blank=True, null=True)
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField(blank=True, null=True)
    km_odometro = models.IntegerField(blank=True, null=True)  # solo cabezales
    costo_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      blank=True, null=True)
    fecha_pago = models.DateField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Mantenimiento'

    def __str__(self):
        activo = self.activo or self.remolque
        return f'{activo} - {self.tipo} - {self.fecha_entrada}'


# =============================================
# DETALLE DE MANTENIMIENTO
# =============================================
class DetalleMantenimiento(models.Model):
    mantenimiento = models.ForeignKey(Mantenimiento, on_delete=models.CASCADE)
    trabajo = models.ForeignKey(TipoTrabajo, on_delete=models.PROTECT)
    config = models.ForeignKey(ConfiguracionMantenimiento, on_delete=models.PROTECT,
                               blank=True, null=True)  # null si tipo_control = 'libre'
    observacion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'DetalleMantenimiento'
        

    def __str__(self):
        return f'{self.mantenimiento} - {self.trabajo}'


# =============================================
# INSUMOS
# =============================================
class InsumoDetalle(models.Model):
    detalle = models.ForeignKey(DetalleMantenimiento, on_delete=models.CASCADE)
    nombre_insumo = models.CharField(max_length=250)
    cantidad = models.DecimalField(max_digits=8, decimal_places=2)
    unidad = models.CharField(max_length=20, blank=True, null=True)
    costo_unitario = models.DecimalField(max_digits=8, decimal_places=2,
                                         blank=True, null=True)

    class Meta:
        db_table = 'InsumoDetalle'
        

    def __str__(self):
        return f'{self.nombre_insumo} - {self.cantidad} {self.unidad}'


# =============================================
# CARGA DE COMBUSTIBLE
# =============================================
class CargaCombustible(models.Model):
    activo = models.ForeignKey(Activo, on_delete=models.CASCADE)
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    fecha = models.DateField()
    km_odometro = models.IntegerField()
    litros = models.DecimalField(max_digits=8, decimal_places=2)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'CargaCombustible'
        

    def __str__(self):
        return f'{self.activo} - {self.fecha} - {self.litros}L'


# =============================================
# KM MANUAL
# =============================================
class KmManual(models.Model):
    activo = models.ForeignKey(Activo, on_delete=models.CASCADE)
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    fecha = models.DateField()
    km_odometro = models.IntegerField()
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'KmManual'
        

    def __str__(self):
        return f'{self.activo} - {self.fecha} - {self.km_odometro} km'