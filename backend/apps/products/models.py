from django.db import models
from django.conf import settings

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)

    estado = models.BooleanField(default=False)

    class Meta:
        db_table = 'categorias'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nombre

class Marca(models.Model):
    id_marca = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)

    estado = models.BooleanField(default=False)

    class Meta:
        db_table = 'marcas'
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'

    def __str__(self):
        return self.nombre

class UnidadMedida(models.Model):
    id_unid_medida = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50) 
    abreviatura = models.CharField(max_length=10)

    estado = models.BooleanField(default=False) 

    class Meta:
        db_table = 'unidades_medida'
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de Medida'

    def __str__(self):
        return f"{self.nombre} ({self.abreviatura})"
    
class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    
    id_categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    id_marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    id_unid_medida = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT)
    
    codigo_barra = models.CharField(max_length=50, unique=True)
    imagen_url = models.ImageField(upload_to='productos/', null=True, blank=True)
    nombre = models.CharField(max_length=250)
    proximo_vencimiento = models.DateField(null=True, blank=True)

    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    porcentaje_ganancia = models.DecimalField(max_digits=5, decimal_places=2, default=30.00)

    stock_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock_maximo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    estado = models.BooleanField(default=True)
    
    # Auditoria
    id_usuario_alta = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos_creados')
    fh_alta = models.DateTimeField(auto_now_add=True)
    id_usuario_baja = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos_eliminados')
    fh_baja = models.DateTimeField(null=True, blank=True)
    id_usuario_modificacion = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos_modificados')
    fh_modificacion = models.DateTimeField(auto_now=True)

    # Clase meta
    class Meta:
        db_table = 'productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return f"[{self.codigo_barra}] {self.nombre}"

class Promocion(models.Model):
    id_promocion = models.AutoField(primary_key=True)

    id_producto = models.ForeignKey('Producto', on_delete=models.CASCADE, null=True, blank=True)
    
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=[('MULTIPLE', 'Por Cantidad (2x1, 3x2)'),('PORCENTAJE', 'Descuento %'),('PRECIO_FIJO', 'Precio de Oferta'),])
    cantidad_requerida = models.IntegerField(default=1)
    unidades_bonificadas = models.IntegerField(default=0)
    porcentaje_descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    
    estado = models.BooleanField(default=True)
    
    # Clase meta
    class Meta:
        db_table = 'promociones'
        verbose_name = 'Promocion'
        verbose_name_plural = 'Promociones'

    def __str__(self):
        return self.nombre