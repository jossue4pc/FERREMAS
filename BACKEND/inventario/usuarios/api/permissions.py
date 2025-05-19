from rest_framework import permissions

class DebugIsAdminUser(permissions.BasePermission):
    """
    Custom permission to debug IsAdminUser.
    Allows access only to admin users (is_staff=True).
    """

    def has_permission(self, request, view):
        print("--- DebugIsAdminUser: Verificando permiso ---")
        print(f"Usuario de la petición (request.user): {request.user}")
        print(f"request.user.is_authenticated: {request.user.is_authenticated}")
        is_staff = getattr(request.user, 'is_staff', False)
        print(f"request.user.is_staff: {is_staff}")
        print("--- DebugIsAdminUser: Fin de logs ---")
        return bool(request.user and request.user.is_authenticated and is_staff)
