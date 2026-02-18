from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Compra, DetalleCompra
from apps.boxes.models import MovimientoCaja

# POST_SAVE''
@receiver(post_save, sender=Compra)
def gestionar_pago_y_anulacion_compra(sender, instance, created, **kwargs):
    """
    Controla el egreso de dinero al comprar y el reingreso si se anula la compra.
    """
    if created and instance.estado == 'RECIBIDA' and instance.metodo_pago == 'EFECTIVO':
        if instance.id_caja:
            MovimientoCaja.objects.create(
                id_caja=instance.id_caja,
                id_compra=instance,
                id_usuario=instance.id_usuario_alta,
                tipo_movimiento='EGRESO',
                monto=instance.total_compra,
                motivo=f"Compra a Proveedor: {instance.id_proveedor.nombre_empresa} - Fact: {instance.numero_factura}",
                origen='COMPRA'
            )

    elif not created and instance.estado == 'ANULADA':
        ya_anulada_caja = MovimientoCaja.objects.filter(
            id_compra=instance, 
            tipo_movimiento='INGRESO',
            origen='COMPRA'
        ).exists()

        if not ya_anulada_caja and instance.id_caja:
            MovimientoCaja.objects.create(
                id_caja=instance.id_caja,
                id_compra=instance,
                id_usuario=instance.id_usuario_baja or instance.id_usuario_modificacion,
                tipo_movimiento='INGRESO',
                monto=instance.total_compra,
                motivo=f"ANULACIÓN Compra #{instance.id_compra} - Reintegro",
                origen='COMPRA'
            )

            detalles = instance.detalles.all()
            for detalle in detalles:
                producto = detalle.id_producto
                producto.stock_actual -= detalle.cantidad
                producto.save()

@receiver(post_save, sender=DetalleCompra)
def aumentar_stock_al_comprar(sender, instance, created, **kwargs):
    """
    Suma stock cuando se registra un producto en el detalle de la compra.
    """
    if created:
        producto = instance.id_producto
        producto.stock_actual += instance.cantidad
        producto.save()

# POST_DELETE''
@receiver(post_delete, sender=DetalleCompra)
def corregir_stock_por_borrado_compra(sender, instance, **kwargs):
    """
    Si se borra un item del detalle de compra, se resta del stock.
    """
    producto = instance.id_producto
    producto.stock_actual -= instance.cantidad
    producto.save()