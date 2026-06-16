from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils import timezone



# =========================
# FORMULARIO WEB
# =========================
class FormularioWeb(models.Model):
    id_formweb = models.AutoField(primary_key=True)
    nombre_formweb = models.CharField(max_length=100)
    email_formweb = models.EmailField()
    tlfno_formweb = models.CharField(max_length=10)
    nomempre_formweb = models.CharField(max_length=250)
    servicio_formweb = models.CharField(max_length=250, null=True, blank=True)
    mensaje_formweb = models.TextField()
    fecha_formweb = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'FormularioWeb'


# =========================
# USUARIO (CUSTOM USER)
# =========================
class Usuario(AbstractUser):
    rol = models.CharField(
        max_length=20,
        choices=[
            ('superadmin', 'Super Administrador'),
            ('admin', 'Administrador'),
            ('conductor', 'Conductor'),
        ],
        default='conductor'
    )

    # Necesario cuando se hereda AbstractUser
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuarios',
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuarios_permisos',
        blank=True
    )

    email = models.EmailField(unique=True, blank=False, null=False)

    class Meta:
        db_table = 'usuarios'


# =========================
# CONDUCTOR
# =========================

class Conductor(models.Model):

    LICENCIAS_ECUADOR = [
        ('C', 'Tipo C '),
        ('D', 'Tipo D '),
        ('E', 'Tipo E '),
    ]

    id_cond = models.AutoField(primary_key=True)

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        db_column='usuario_id'
    )

    nombres_cond = models.CharField(max_length=150)
    apell_cond = models.CharField(max_length=150)
    cedla_cond = models.CharField(max_length=150, unique=True)

    tipolicen_cond = models.CharField(
        max_length=3,
        choices=LICENCIAS_ECUADOR
    )

    telfno_cond = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = 'conductor'
        managed = False




# =========================
# MARCA TRAILER
# =========================
class MarcaTrailer(models.Model):
    id_marca = models.AutoField(primary_key=True)
    nombre_marca = models.CharField(max_length=200, unique=True)

    class Meta:
        db_table = 'MarcaTrailer'
        managed = False


# =========================
# CONFIGURACIÓN MANTENIMIENTO
# =========================
class ConfiguracionMantenimiento(models.Model):
    id_config = models.AutoField(primary_key=True)

    marca = models.ForeignKey(
        MarcaTrailer,
        on_delete=models.PROTECT,
        db_column='marca_id'
    )

    tipo_trabajo = models.CharField(max_length=250)
    kilome_intervalo = models.IntegerField()

    class Meta:
        db_table = 'ConfiguracionMantenimiento'
        managed = False


# =========================
# TRAILER
# =========================
class Trailer(models.Model):
    id_trai = models.AutoField(primary_key=True)
    placa_trai = models.CharField(max_length=8, unique=True)

    marca = models.ForeignKey(
        MarcaTrailer,
        on_delete=models.PROTECT,
        db_column='marca_id'
    )

    anio_trai = models.IntegerField()
    numotor_trai = models.CharField(max_length=50, unique=True)
    numchasis_trai = models.CharField(max_length=50, unique=True)
    numdisco_trai = models.CharField(max_length=5)
    kilometraje_actual = models.IntegerField()
    fechcaduc_trai = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'Trailer'
        managed = False


# =========================
# MANTENIMIENTO TRAILER
# =========================
class MantenimientoTrailer(models.Model):
    id_mantrai = models.AutoField(primary_key=True)

    trailer = models.ForeignKey(
        Trailer,
        on_delete=models.PROTECT,
        db_column='trailer_id'
    )

    conductor = models.ForeignKey(
        Conductor,
        on_delete=models.PROTECT,
        db_column='conductor_id'
    )

    kilometraje = models.IntegerField()
    fecha_mantrai = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'MantenimientoTrailer'
        managed = False


# =========================
# DETALLE MANTENIMIENTO
# =========================
class DetalleManTrailer(models.Model):
    id_detamantrai = models.AutoField(primary_key=True)

    mantrailer = models.ForeignKey(
        MantenimientoTrailer,
        on_delete=models.PROTECT,
        db_column='mantrailer_id'
    )

    config = models.ForeignKey(
        ConfiguracionMantenimiento,
        on_delete=models.PROTECT,
        db_column='id_config'
    )

    class Meta:
        db_table = 'DetalleManTrailer'
        managed = False


# =========================
# INSUMOS DETALLE
# =========================
class InsumoDetalleTrailer(models.Model):
    id_insumotrai = models.AutoField(primary_key=True)

    detalle = models.ForeignKey(
        DetalleManTrailer,
        on_delete=models.PROTECT,
        db_column='detalltrai_id'
    )

    nombre_insumo = models.CharField(max_length=250)
    cantidad = models.IntegerField()
    costo_unitario = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'InsumoDetalleTrailer'
        managed = False


# =========================
# BITÁCORA
# =========================
class BitacoraAcciones(models.Model):
    id_bita = models.AutoField(primary_key=True)

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        db_column='usuario_id'
    )

    accion = models.CharField(max_length=100)
    modulo = models.CharField(max_length=50)
    regist_modif = models.IntegerField()

    valor_anter = models.JSONField(null=True, blank=True)
    valor_nuevo = models.JSONField(null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'BitacoraAcciones'
        managed = False


# =========================
# CÓDIGO DE RECUPERACIÓN
# =========================
class CodigoRecuperacion(models.Model):
    id_codigo = models.AutoField(primary_key=True)

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='usuario_id'
    )

    codigo = models.CharField(max_length=6)
    creado = models.DateTimeField(auto_now_add=True)
    valido_hasta = models.DateTimeField()

    def es_valido(self):
        valido_hasta = self.valido_hasta

        # 🔥 Evita el error naive vs aware
        if timezone.is_naive(valido_hasta):
            valido_hasta = timezone.make_aware(valido_hasta)

        return timezone.now() <= valido_hasta

    class Meta:
        db_table = 'codigorecuperacion'
        managed = False


