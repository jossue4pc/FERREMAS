from django.db import models

# Create your models here.
class producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.FloatField()
    cantidad = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    stock = models.IntegerField(default=0)
    categoria = models.CharField(max_length=50, default='general')
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True) # Campo para la imagen

    def __str__(self):
        return self.nombre
