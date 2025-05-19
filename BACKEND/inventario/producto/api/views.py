from rest_framework import viewsets, filters
from producto.models import producto # Cambiado a 'producto' con 'p' minúscula
from producto.api.serializers import ProductoSerializer



class productoViewSet(viewsets.ModelViewSet): # Cambiado a 'productoViewSet' con 'p' minúscula para coincidir con el modelo
    serializer_class = ProductoSerializer
    queryset = producto.objects.all() # Cambiado a 'producto' con 'p' minúscula
    filter_backends = [filters.SearchFilter, filters.OrderingFilter] # <--- Añade SearchFilter
    search_fields = ['nombre', 'descripcion', 'categoria'] # <--- Define en qué campos buscar
    ordering_fields = ['nombre', 'precio', 'cantidad'] # Opcional: para ordenar
