"""
URL configuration for inventario project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings # <--- Añade esta importación
from django.conf.urls.static import static # <--- Añade esta importación
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('producto.api.urls')),
    path('api/auth/', include('usuarios.urls')), # Incluye las URLs de la app usuarios (login, etc.)
]

# Sirve archivos multimedia en desarrollo (solo si DEBUG es True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Opcional: Si también necesitas servir archivos estáticos de esta manera (generalmente no es necesario con runserver)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
