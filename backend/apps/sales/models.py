from django.db import models
from django.conf import settings

class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    
    id_cliente = models.ForeignKey('customers.Cliente', on_delete=models.PROTECT, related_name='compras_cliente')
    id_caja = models.ForeignKey('boxes.Caja', on_delete=models.PROTECT, related_name='ventas_caja')
    
    fh_venta = models.DateTimeField(auto_now_add=True)
    total_venta = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    monto_recibido = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    vuelto = models.DecimalField(max_digits=12, decimal_places=2, default=0.00) 
    descuento_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    METODO_PAGO_CHOICES = [('EFECTIVO', 'Efectivo'),('TRANSFERENCIA', 'Transferencia'),('TARJETA', 'Tarjeta'),]
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES, default='EFECTIVO')
  
    # Auditoria
    ESTADO_CHOICES = [('COMPLETADA', 'Completada'),('ANULADA', 'Anulada'),]
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='COMPLETADA')

    id_usuario_alta = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='ventas_realizadas')
    fh_alta = models.DateTimeField(auto_now_add=True)
    id_usuario_modificacion = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='ventas_modificadas')
    fh_modificacion = models.DateTimeField(auto_now=True)
    id_usuario_baja = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='ventas_anuladas')
    fh_baja = models.DateTimeField(null=True, blank=True)
    observacion = models.TextField(null=True, blank=True)

    # Clase meta
    class Meta:
        db_table = 'ventas'
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'

    def __str__(self):
        return f"Ticket #{self.id_venta} - {self.total_venta}"

# Detalle De Venta
class DetalleVenta(models.Model):
    id_detalle_venta = models.AutoField(primary_key=True)
    
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    id_producto = models.ForeignKey('products.Producto', on_delete=models.PROTECT, related_name='detalles_venta')
    id_promocion = models.ForeignKey('products.Promocion', on_delete=models.SET_NULL, null=True, blank=True)
    
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio_costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, help_text="Costo de compra en el momento de la venta")
    monto_descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,help_text="Monto total restado por promociones")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    #Clase meta
    class Meta:
        db_table = 'detalles_venta'
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalles de Ventas'

    def __str__(self):
        return f"Venta {self.id_venta_id} - {self.id_producto.nombre} x {self.cantidad}"
