from django.db import models
from django.conf import settings

class Compra(models.Model):
    id_compra = models.AutoField(primary_key=True)
    
    id_caja = models.ForeignKey(
        'boxes.Caja', 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True,
        verbose_name="Caja de Pago",
        help_text="Caja de la cual sale el efectivo"
    )
    id_proveedor = models.ForeignKey('suppliers.Proveedor', on_delete=models.PROTECT, related_name='compras')
    
    fh_compra = models.DateTimeField(auto_now_add=True)
    numero_factura = models.CharField(max_length=50, help_text="Número de comprobante del proveedor")
    total_compra = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    ESTADO_CHOICES = [
        ('RECIBIDA', 'Recibida'),
        ('PENDIENTE', 'Pendiente de Entrega'),
        ('ANULADA', 'Anulada'),
    ]
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='RECIBIDA')
    
    metodo_pago = models.CharField(max_length=20, choices=[
        ('EFECTIVO', 'Efectivo'),
        ('CREDITO', 'Crédito / Cuenta Corriente'),
        ('TRANSFERENCIA', 'Transferencia'),
    ], default='EFECTIVO')

    # Auditoría
    id_usuario_alta = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='compras_creadas')
    fh_alta =models.DateTimeField(auto_now_add=True)
    id_usuario_baja = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='compras_anuladas')
    fh_baja = models.DateTimeField(null=True, blank=True)
    id_usuario_modificacion = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='compras_modificadas')
    fh_modificacion = models.DateTimeField(auto_now=True)
    observaciones = models.TextField(null=True, blank=True)

    #Clase meta
    class Meta:
        db_table = 'compras'
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'

    def __str__(self):
        return f"Compra #{self.id_compra} - Factura: {self.numero_factura}"

class DetalleCompra(models.Model):
    id_detalle_compra = models.AutoField(primary_key=True)

    id_compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='detalles')
    id_producto = models.ForeignKey('products.Producto', on_delete=models.PROTECT)
    
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_costo_anterior = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Precio de costo antes de esta compra para ver variaciones"
    )
    precio_compra_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta_sugerido = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    lote = models.CharField(max_length=50, null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)

    #Clase meta
    class Meta:
        db_table = 'detalles_compra'
        verbose_name = 'Detalle de Compra'
        verbose_name_plural = 'Detalles de Compra'

    def __str__(self):
        return f"{self.id_producto.nombre} x {self.cantidad}"