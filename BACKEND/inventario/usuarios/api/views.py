from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import generics, permissions, viewsets # <--- Modifica esta importación
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, AuthTokenSerializer, AdminUserSerializer # No se importa DebugIsAdminUser aquí, se importa en el siguiente cambio
from .permissions import DebugIsAdminUser # <--- Importa AdminUserSerializer

class CustomAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer # Usamos nuestro serializador personalizado para la validación

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_data = UserSerializer(user).data # Serializamos el objeto User
        return Response({
            'token': token.key,
            'user': user_data # Incluimos los datos del usuario serializados
        })

User = get_user_model() # Obtener el modelo User activo

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] # CORREGIDO: Cualquiera puede acceder a este endpoint para registrarse

# ViewSet para la gestión de usuarios por administradores
class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id') # Obtener todos los usuarios, ordenados por ID
    serializer_class = AdminUserSerializer
    permission_classes = [DebugIsAdminUser] # CORREGIDO: Usa la clase de permiso personalizada para depuración

    # Podrías añadir lógica personalizada aquí si es necesario, por ejemplo, para la creación o actualización.
    def list(self, request, *args, **kwargs):
        print("--- AdminUserViewSet: Entrando a list ---")
        print(f"Usuario de la petición (request.user): {request.user}")
        print(f"request.user.is_authenticated: {request.user.is_authenticated}")
        if hasattr(request.user, 'is_staff'):
            print(f"request.user.is_staff: {request.user.is_staff}")
        if hasattr(request.user, 'is_superuser'):
            print(f"request.user.is_superuser: {request.user.is_superuser}")
        print(f"Token de autenticación (request.auth): {request.auth}")
        print("--- AdminUserViewSet: Fin de logs en list ---")
        return super().list(request, *args, **kwargs)