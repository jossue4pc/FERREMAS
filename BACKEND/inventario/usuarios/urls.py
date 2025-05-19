from django.urls import path, include # <--- Añade include
from rest_framework.routers import DefaultRouter # <--- Importa DefaultRouter
from .api.views import CustomAuthToken, UserCreateView, AdminUserViewSet # <--- Importa AdminUserViewSet

# Crear un router y registrar nuestro ViewSet
router = DefaultRouter()
router.register(r'admin/users', AdminUserViewSet, basename='admin-user') # El prefijo será 'admin/users'

app_name = 'usuarios_api' # Opcional, pero buena práctica para namespacing
urlpatterns = [
    path('login/', CustomAuthToken.as_view(), name='login'), # Endpoint para el login personalizado
    path('register/', UserCreateView.as_view(), name='register'), # <--- Añade esta línea para el registro
    path('', include(router.urls)), # <--- Incluye las URLs generadas por el router
]