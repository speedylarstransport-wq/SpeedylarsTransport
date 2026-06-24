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


