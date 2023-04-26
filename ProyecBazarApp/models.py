from django.db import models
from django.contrib.auth.models import AbstractUser
# son para borrar imagen al actualizar
import os
from django.dispatch import receiver
from django.db.models.signals import pre_save

from .choices import estadoDia
# Create your models here.

class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    rol_usuario = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.rol_usuario}"

class Region(models.Model):
    id_regiones = models.AutoField(primary_key=True)
    nombre_region = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return f"{self.nombre_region}"

class Comuna(models.Model):
    id_comuna = models.AutoField(primary_key=True)
    nombre_comuna = models.CharField(max_length=45)
    region_FK = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre_comuna}"

class Usuario(AbstractUser):
    rol_FK = models.ForeignKey(Rol, on_delete=models.CASCADE)
    comuna_FK = models.ForeignKey(Comuna, on_delete=models.CASCADE)

    
class TipoGiro(models.Model):
    id_giro = models.AutoField(primary_key=True)
    nombre_giro = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return f"{self.nombre_giro}"

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    run_cliente = models.CharField(max_length=15, unique=True)
    nombre_cliente = models.CharField(max_length=45)
    apellido_cliente = models.CharField(max_length=45)
    razon_social_cliente = models.CharField(max_length=45)
    direccion = models.CharField(max_length=45)
    comuna_FK = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    tipo_giro_FK = models.ForeignKey(TipoGiro, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre_cliente} {self.apellido_cliente}"

class Marca(models.Model):
    id_marca = models.AutoField(primary_key=True)
    nombre_marca = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.nombre_marca}"

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.nombre_categoria}"

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    codigo_producto = models.CharField(max_length=45,unique=True)
    nombre_producto = models.CharField(max_length=45)
    precio_producto = models.IntegerField()
    imagen = models.ImageField(upload_to='productos')
    marca_FK = models.ForeignKey(Marca, on_delete=models.CASCADE)
    usuario_FK = models.ForeignKey(Usuario, on_delete=models.CASCADE,default=4)
    categoria_FK = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre_producto}"
    
    def borrar_imagen_anterior(self):
        # Si se está actualizando un objeto del modelo y tiene una imagen anterior,
        # borramos la imagen anterior antes de guardar la nueva imagen.
        if self.id_producto is not None:
            try:
                producto_anterior = Producto.objects.get(id_producto=self.id_producto)
                if producto_anterior.imagen != self.imagen:
                    os.remove(producto_anterior.imagen.path)
            except Producto.DoesNotExist:
                pass
            
@receiver(pre_save, sender=Producto)
def borrar_imagen_anterior(sender, instance, **kwargs):
    instance.borrar_imagen_anterior()

class Facturas(models.Model):
    id_factura = models.AutoField(primary_key=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    total_factura = models.IntegerField()
    usuario_FK = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id_factura}"

class DetalleFacturas(models.Model):
    id_detalle_factura = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    total = models.IntegerField()
    producto_FK = models.ForeignKey(Producto, on_delete=models.CASCADE)
    factura_FK = models.ForeignKey(Facturas, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id_detalle_factura}"

class Boletas(models.Model):
    id_boleta = models.AutoField(primary_key=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    total_boleta = models.IntegerField()
    usuario_FK = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id_boleta}"

class DetalleBoletas(models.Model):
    id_detalle_boleta = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    total = models.IntegerField()
    producto_FK = models.ForeignKey(Producto, on_delete=models.CASCADE)
    boleta_FK = models.ForeignKey(Boletas, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id_detalle_boleta}"

class DatosEmpresa(models.Model):
    id_datos_empresa = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=45)
    rut_empresa = models.CharField(max_length=15)
    direccion_empresa = models.CharField(max_length=45)
    IVA = models.IntegerField()
    estado = models.IntegerField(choices=estadoDia,default=1)

    def __str__(self):
        return f"{self.nombre_empresa}"
