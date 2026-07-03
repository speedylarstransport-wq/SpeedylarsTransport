from functools import wraps
from django.core.exceptions import PermissionDenied

def rol_requerido(roles_permitidos):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            print("Usuario:", request.user)
            print("Rol:", request.user.rol)
            print("Roles permitidos:", roles_permitidos)

            if request.user.is_authenticated and request.user.rol in roles_permitidos:
                return view_func(request, *args, **kwargs)

            raise PermissionDenied("No tiene permisos para acceder.")

        return wrapper
    return decorator