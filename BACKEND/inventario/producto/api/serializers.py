from producto.models import producto
from rest_framework import serializers

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'cantidad', 'categoria', 'imagen']
