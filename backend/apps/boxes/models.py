from django.db import models
from django.conf import settings

class Caja(models.Model):
    id_caja = models.AutoField(primary_key=True)
    
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,related_name='cajas_sesiones')
    
    monto_inicial = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    monto_final_sistema = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    monto_final_real = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    monto_diferencia = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    estado = models.BooleanField(default=True)
    fh_apertura = models.DateTimeField(auto_now_add=True)
    fh_cierre = models.DateTimeField(null=True, blank=True)
    observacion = models.TextField(null=True, blank=True)
    
    # Clase Meta
    class Meta:
        db_table = 'cajas'
        verbose_name = 'Caja'
        verbose_name_plural = 'Cajas'

    def __str__(self):
        estado_str = "Abierta" if self.estado else "Cerrada"
        return f"Caja #{self.id_caja} - {self.id_usuario.username} ({estado_str})"

class MovimientoCaja(models.Model):
    id_mov_caja = models.AutoField(primary_key=True)
    
    id_venta = models.ForeignKey('sales.Venta', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Venta Relacionada")
    id_compra = models.ForeignKey('purchases.Compra', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Compra Relacionada")
    id_caja = models.ForeignKey(Caja, on_delete=models.CASCADE, related_name='movimientos')
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,related_name='movimientos_caja')

    TIPO_CHOICES = [('INGRESO', 'Ingreso'),('EGRESO', 'Egreso'),]
    tipo_movimiento = models.CharField(max_length=10, choices=TIPO_CHOICES)

    monto = models.DecimalField(max_digits=10, decimal_places=2)
    motivo = models.CharField(max_length=255)

    ORIGEN_CHOICES =[('VENTA', 'Venta'), ('COMPRA', 'Compra'), ('MANUAL', 'Ajuste Manual'),('GASTO', 'Gasto Operativo')]
    origen = models.CharField(max_length=20, choices=ORIGEN_CHOICES, default='MANUAL')
    
    fh_creacion = models.DateTimeField(auto_now_add=True)
    id_usuario_creacion = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='movcaja_creados')
    fh_actualizacion = models.DateTimeField(auto_now=True)
    id_usuario_actualizacion = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='movcaja_actualizados')
    
    # Clase Meta
    class Meta:
        db_table = 'movimientos_caja'
        verbose_name = 'Movimiento de la Caja'
        verbose_name_plural = 'Movimientos de la caja'

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.monto} ({self.motivo})"
