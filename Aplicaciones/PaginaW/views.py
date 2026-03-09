from django.shortcuts import render

# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')

def quienesomos(request):
    return render(request, 'quienesomos.html')

def servicios(request):
    return render(request, 'servicios.html')

def contactanos(request):
    return render(request, 'contactanos.html')



def error_404(request, url=None):
    return render(request, '404.html', status=404)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings



def login_view(request):
    # Si ya inició sesión, no volver al login
    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip().lower()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                # 🔁 Redirección si viene de @login_required
                next_url = request.POST.get('next') or request.GET.get('next')
                if next_url:
                    return redirect(next_url)

                messages.success(request, f'Bienvenido/a {user.first_name}')
                return redirect('inicio')
            else:
                messages.warning(
                    request,
                    'Tu cuenta está desactivada. Contacta al administrador.'
                )
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('login')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

from .models import Usuario, Conductor
from .forms import UsuarioForm, ConductorForm



# =====================================================
# REGISTRAR USUARIO
# =====================================================
#@login_required
#@rol_requerido(['admin', 'superadmin'])
def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Usuario registrado correctamente.")
                return redirect('lista_usuarios')
            except Exception as e:
                messages.error(request, f"Error al guardar: {str(e)}")
        else:
            # Para debugging: imprimir errores en consola
            print("Errores del formulario:", form.errors)
            messages.error(request, "Error al registrar el usuario. Verifique los campos.")
    else:
        form = UsuarioForm()

    return render(request, 'registrar.html', {
        'form': form
    })

# =====================================================
# LISTA DE USUARIOS
# =====================================================
#@login_required
#@rol_requerido(['admin', 'superadmin'])
def lista_usuarios(request):
    usuarios = Usuario.objects.all().order_by('id')
    return render(request, 'usuarios/lista_usuarios.html', {
        'usuarios': usuarios
    })


# =====================================================
# EDITAR USUARIO
# =====================================================
#@login_required
#@rol_requerido(['admin', 'superadmin'])
def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, pk=id)

    if request.method == 'POST':

        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        rol = request.POST.get('rol')

        # ================= VALIDACIONES =================

        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', first_name):
            return redirect(f"{reverse('lista_usuarios')}?error=1&usuario_id={usuario.id}&msg=Nombre inválido")

        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', last_name):
            return redirect(f"{reverse('lista_usuarios')}?error=1&usuario_id={usuario.id}&msg=Apellido inválido")

        try:
            validate_email(username)
            if '.' not in username.split('@')[-1]:
                raise ValidationError
        except ValidationError:
            return redirect(f"{reverse('lista_usuarios')}?error=1&usuario_id={usuario.id}&msg=Usuario inválido")

        try:
            validate_email(email)
            if '.' not in email.split('@')[-1]:
                raise ValidationError
        except ValidationError:
            return redirect(f"{reverse('lista_usuarios')}?error=1&usuario_id={usuario.id}&msg=Correo inválido")

        # ================= ACTUALIZAR =================

        usuario.first_name = first_name.title()
        usuario.last_name = last_name.title()
        usuario.username = username.lower()
        usuario.email = email.lower()

        # ================= ROL =================
        if rol in ['superadmin', 'admin', 'conductor']:
            usuario.rol = rol

            if rol == 'superadmin':
                usuario.is_staff = True
                usuario.is_superuser = True
            elif rol == 'admin':
                usuario.is_staff = True
                usuario.is_superuser = False
            else:
                usuario.is_staff = False
                usuario.is_superuser = False

        # ================= ACTIVO =================
        usuario.is_active = True if request.POST.get('is_active') == 'on' else False

        # ================= CONTRASEÑA =================
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password or password_confirm:
            if password != password_confirm:
                return redirect(
                    f"{reverse('lista_usuarios')}?error=1&usuario_id={usuario.id}&msg=Las contraseñas no coinciden"
                )
            usuario.set_password(password)

        usuario.save()

        return redirect(
            f"{reverse('lista_usuarios')}?success=1&msg=Usuario actualizado correctamente"
        )

    return redirect('lista_usuarios')


# =====================================================
# ELIMINAR USUARIO
# =====================================================
#@login_required
#@rol_requerido(['admin', 'superadmin'])
def eliminar_usuario(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    nombre = usuario.get_full_name() or usuario.username
    usuario.delete()

    messages.success(request, f'Usuario "{nombre}" eliminado correctamente.')
    return redirect('lista_usuarios')




def nuevo_conductor(request):
    """
    Vista para crear un nuevo conductor.
    """

    if request.method == 'POST':
        form = ConductorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Conductor registrado exitosamente!")
            return redirect('nuevo_conductor')  # Puedes cambiar la URL según tu urls.py
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = ConductorForm()

    context = {
        'form': form
    }
    return render(request, 'conductor/nuevoConductor.html', context)







# =========================
# LISTADO DE CONDUCTORES
# =========================
#@login_required
def listado_conductor(request):
    conductores = Conductor.objects.select_related('usuario').all()

    return render(request, 'conductor/listadoConductor.html', {
        'conductores': conductores
    })



def editar_conductor(request, id):
    conductor = get_object_or_404(Conductor, id_cond=id)

    if request.method == 'POST':
        conductor.nombres_cond = request.POST.get('nombres_cond')
        conductor.apell_cond = request.POST.get('apell_cond')
        conductor.telfno_cond = request.POST.get('telfno_cond')
        conductor.save()
        messages.success(request, 'Conductor actualizado correctamente')

    return redirect('listado_conductor')


# =========================
# DESACTIVAR CONDUCTOR
# =========================
#@login_required
def desactivar_conductor(request, id):
    conductor = get_object_or_404(Conductor, id_cond=id)
    usuario = conductor.usuario

    usuario.is_active = False
    usuario.save()

    messages.warning(request, 'Conductor desactivado correctamente')
    return redirect('listado_conductor')


# =========================
# ACTIVAR CONDUCTOR
# =========================
#@login_required
def activar_conductor(request, id):
    conductor = get_object_or_404(Conductor, id_cond=id)
    usuario = conductor.usuario

    usuario.is_active = True
    usuario.save()

    messages.success(request, 'Conductor activado correctamente')
    return redirect('listado_conductor')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail

from .models import Usuario, CodigoRecuperacion

from datetime import timedelta
import random
import string


# =========================
# GENERAR CÓDIGO ALEATORIO
# =========================
def generar_codigo():
    return ''.join(random.choices(string.digits, k=6))


# =========================
# RECUPERAR CONTRASEÑA
# =========================
def recuperar_contrasena(request):
    context = {}

    if request.method == 'POST':
        paso = request.POST.get('paso')
        email = request.POST.get('email', '').strip().lower()
        context['email'] = email

        # 🔹 BUSCAR USUARIO (CUSTOM USER)
        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            messages.error(request, "No se encontró ningún usuario con ese correo.")
            return render(request, 'recuperar_contrasena.html', context)

        # =========================
        # PASO 1 → ENVIAR CÓDIGO
        # =========================
        if paso == '1':
            codigo = generar_codigo()
            expira = timezone.now() + timedelta(minutes=15)

            # Eliminar códigos anteriores
            CodigoRecuperacion.objects.filter(usuario=usuario).delete()

            # Crear nuevo código
            CodigoRecuperacion.objects.create(
                usuario=usuario,
                codigo=codigo,
                valido_hasta=expira
            )

            try:
                send_mail(
                    'Código de recuperación de contraseña',
                    f'Tu código de recuperación es: {codigo}\n\nEste código vence en 15 minutos.',
                    settings.EMAIL_HOST_USER,
                    [usuario.email],
                    fail_silently=False,
                )
                messages.success(request, "Se ha enviado un código a tu correo.")
                context['mostrar_formulario_codigo'] = True

            except Exception as e:
                messages.error(request, "No se pudo enviar el correo. Intenta más tarde.")
                print("Error correo:", e)

        # =========================
        # PASO 2 → VALIDAR CÓDIGO
        # =========================
        elif paso == '2':
            codigo = request.POST.get('codigo', '').strip()
            nueva_contrasena = request.POST.get('nueva_contrasena', '').strip()
            confirmar_contrasena = request.POST.get('confirmar_contrasena', '').strip()

            context['mostrar_formulario_codigo'] = True
            context['codigo'] = codigo

            if nueva_contrasena != confirmar_contrasena:
                messages.error(request, "Las contraseñas no coinciden.")
                return render(request, 'recuperar_contrasena.html', context)

            try:
                codigo_obj = CodigoRecuperacion.objects.get(
                    usuario=usuario,
                    codigo=codigo
                )

                if codigo_obj.es_valido():
                    usuario.set_password(nueva_contrasena)
                    usuario.save()
                    codigo_obj.delete()

                    messages.success(request, "Contraseña actualizada correctamente.")
                    return redirect('login')
                else:
                    messages.error(request, "El código ha expirado.")

            except CodigoRecuperacion.DoesNotExist:
                messages.error(request, "Código incorrecto.")

    return render(request, 'recuperar_contrasena.html', context)
