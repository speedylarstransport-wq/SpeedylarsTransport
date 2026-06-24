from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Usuario
import re


class UsuarioForm(UserCreationForm):
    # Solo email como campo principal
    email = forms.EmailField(
        label="Correo Electrónico",
        help_text="Este correo será tu usuario para iniciar sesión",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com',
            'autofocus': True
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
    
    rol = forms.ChoiceField(
        label="Rol del Usuario",
        choices=[
            ('superadmin', 'Super Administrador'),
            ('admin', 'Administrador'),
            ('conductor', 'Conductor'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    # Personalizar los campos de contraseña (requisitos simplificados)
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña'
        }),
        help_text="Mínimo 8 caracteres. Debe incluir una letra mayúscula, una minúscula y un número."
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
            'email',
            'first_name',
            'last_name',
            'rol',
            'password1',
            'password2',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # El campo username existe en el modelo pero lo ocultamos
        # Verificamos si el campo existe antes de modificarlo
        if 'username' in self.fields:
            self.fields['username'].required = False
            self.fields['username'].widget = forms.HiddenInput()

    # ---------- VALIDACIONES ----------
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

        # Validación 1: mínimo 8 caracteres
        if len(password1) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        
        # Validación 2: debe contener al menos una letra mayúscula
        if not re.search(r'[A-Z]', password1):
            raise forms.ValidationError("La contraseña debe contener al menos una letra mayúscula.")
        
        # Validación 3: debe contener al menos una letra minúscula
        if not re.search(r'[a-z]', password1):
            raise forms.ValidationError("La contraseña debe contener al menos una letra minúscula.")
        
        # Validación 4: debe contener al menos un número
        if not re.search(r'[0-9]', password1):
            raise forms.ValidationError("La contraseña debe contener al menos un número.")
        
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
        
        # Usar el email como username también (requerido por AbstractUser)
        user.username = self.cleaned_data['email']
        
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


