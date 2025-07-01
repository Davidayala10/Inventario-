from django.db import models

class DimFecha(models.Model):
    fecha = models.DateField()
    mes = models.IntegerField()
    trimestre = models.IntegerField()
    anio = models.IntegerField()

class DimTienda(models.Model):
    nombre = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    tipo_tienda = models.CharField(max_length=50)

class DimProveedor(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)

class DimCategoria(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    estacionalidad = models.CharField(max_length=50)

class DimProducto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(DimCategoria, on_delete=models.CASCADE)
    unidad_medida = models.CharField(max_length=20)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

class HechosInventario(models.Model):
    tienda = models.ForeignKey(DimTienda, on_delete=models.CASCADE)
    producto = models.ForeignKey(DimProducto, on_delete=models.CASCADE)
    fecha = models.ForeignKey(DimFecha, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(DimProveedor, on_delete=models.CASCADE)
    cantidad_disponible = models.IntegerField()
    cantidad_vendida = models.IntegerField()
    cantidad_reabastecida = models.IntegerField()
