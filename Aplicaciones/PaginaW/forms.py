from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Usuario, Conductor
import re


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
from .models import Usuario
from django.contrib.auth.password_validation import validate_password

class UsuarioForm(UserCreationForm):
    # Personalizar widgets y ayuda
    username = forms.CharField(
        label="Cédula",
        help_text="Número de cédula de 10 dígitos (Ej: 1234567890)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1234567890',
            'maxlength': '10'
        })
    )
    
    first_name = forms.CharField(
        label="Nombres",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: María José'
        })
    )
    
    last_name = forms.CharField(
        label="Apellidos",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: González Pérez'
        })
    )
    
    email = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'speedylars@correo.com'
        })
    )
    
    rol = forms.ChoiceField(
        label="Rol del Usuario",
        choices=[
            ('', 'Seleccione un rol...'),
            ('superadmin', 'Super Administrador'),
            ('admin', 'Administrador'),
            ('conductor', 'Conductor'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    # Personalizar los campos de contraseña
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña'
        }),
        help_text="Mínimo 8 caracteres. No se requieren caracteres especiales."
    )
    
    password2 = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repita su contraseña'
        })
    )
    
    class Meta:
        model = Usuario
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'rol',
            'password1',
            'password2',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar mensajes de ayuda para contraseñas
        self.fields['password1'].help_text = (
            "Tu contraseña debe tener al menos 8 caracteres. "
            "Puede contener letras y números."
        )

    # ---------- VALIDACIONES ----------
    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        
        if not username:
            raise forms.ValidationError("La cédula es obligatoria.")
        
        # Validar que sean solo números
        if not username.isdigit():
            raise forms.ValidationError("La cédula debe contener solo números.")
        
        # Validar que tenga 10 dígitos
        if len(username) != 10:
            raise forms.ValidationError("La cédula debe tener exactamente 10 dígitos.")
        
        # Verificar que no exista ya
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError("Ya existe un usuario con esta cédula.")
        
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()

        if not email:
            raise forms.ValidationError("El correo electrónico es obligatorio.")
            
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Correo electrónico inválido.")
        
        # Verificar que el dominio tenga punto
        if '.' not in email.split('@')[-1]:
            raise forms.ValidationError("El dominio del correo debe contener un punto (ej. ejemplo.com).")
        
        # Verificar que no exista ya
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un usuario con este correo electrónico.")
            
        return email

    def clean_first_name(self):
        nombre = self.cleaned_data.get('first_name', '').strip()
        
        if not nombre:
            raise forms.ValidationError("Los nombres son obligatorios.")
            
        # Permitir espacios y letras con acentos
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', nombre):
            raise forms.ValidationError("Los nombres solo deben contener letras y espacios.")
            
        return nombre.title()

    def clean_last_name(self):
        apellido = self.cleaned_data.get('last_name', '').strip()
        
        if not apellido:
            raise forms.ValidationError("Los apellidos son obligatorios.")
            
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', apellido):
            raise forms.ValidationError("Los apellidos solo deben contener letras y espacios.")
            
        return apellido.title()

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        
        if not password1:
            raise forms.ValidationError("La contraseña es obligatoria.")
        
        # Validación mínima: al menos 8 caracteres
        if len(password1) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        
        # Opcional: Validar que no sea demasiado común
        common_passwords = ['12345678', 'password', 'contraseña', 'admin123', '00000000']
        if password1.lower() in common_passwords:
            raise forms.ValidationError("Por favor, elija una contraseña más segura.")
        
        return password1

    def clean(self):
        cleaned_data = super().clean()
        
        # Validar que el rol no sea vacío
        rol = cleaned_data.get('rol')
        if not rol:
            self.add_error('rol', "Debe seleccionar un rol.")
            
        # Validar que las contraseñas coincidan
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Las contraseñas no coinciden.")
            
        return cleaned_data

    # ---------- GUARDADO ----------
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Todos los usuarios nuevos están activos por defecto
        user.is_active = True
        
        # Configurar flags según rol
        if user.rol == 'superadmin':
            user.is_staff = True
            user.is_superuser = True
        elif user.rol == 'admin': 
            user.is_staff = True
            user.is_superuser = False
        else:  # conductor
            user.is_staff = False
            user.is_superuser = False

        if commit:
            user.save()
            
        return user
    

    
class ConductorForm(forms.ModelForm):
    class Meta:
        model = Conductor
        fields = ['usuario', 'nombres_cond', 'apell_cond', 'cedla_cond', 'tipolicen_cond', 'telfno_cond']

        widgets = {
            'nombres_cond': forms.TextInput(attrs={'placeholder': 'Nombres'}),
            'apell_cond': forms.TextInput(attrs={'placeholder': 'Apellidos'}),
            'cedla_cond': forms.TextInput(attrs={'placeholder': 'Cédula'}),
            'tipolicen_cond': forms.Select(attrs={'placeholder': 'Tipo de licencia'}),
            'telfno_cond': forms.TextInput(attrs={'placeholder': 'Teléfono'}),
        }

    def clean_cedla_cond(self):
        cedula = self.cleaned_data.get('cedla_cond')
        if cedula and len(cedula) != 10:
            raise forms.ValidationError("La cédula debe tener exactamente 10 dígitos.")
        return cedula
