from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Venta, DetalleVenta
from apps.boxes.models import MovimientoCaja

# POST_SAVE
@receiver(post_save, sender=Venta)
def gestionar_transaccion_y_anulacion(sender, instance, created, **kwargs):
    """
    Controla el flujo de dinero y el reingreso de stock por anulación.
    """
    if created and instance.estado == 'COMPLETADA':
        MovimientoCaja.objects.create(
            id_caja=instance.id_caja,
            id_venta=instance,
            id_usuario=instance.id_usuario_alta,
            tipo_movimiento='INGRESO',
            monto=instance.total_venta,
            motivo=f"Venta Ticket #{instance.id_venta}",
            origen='VENTA'
        )

    elif not created and instance.estado == 'ANULADA':
        ya_anulada_caja = MovimientoCaja.objects.filter(
            id_venta=instance, 
            tipo_movimiento='EGRESO',
            origen='VENTA'
        ).exists()

        if not ya_anulada_caja:
            usuario_operacion = instance.id_usuario_baja or instance.id_usuario_modificacion
            
            MovimientoCaja.objects.create(
                id_caja=instance.id_caja,
                id_venta=instance,
                id_usuario=usuario_operacion,
                tipo_movimiento='EGRESO',
                monto=instance.total_venta,
                motivo=f"ANULACIÓN Ticket #{instance.id_venta}",
                origen='VENTA'
            )

            detalles = instance.detalles.all()
            for detalle in detalles:
                producto = detalle.id_producto
                producto.stock_actual += detalle.cantidad
                producto.save()


@receiver(post_save, sender=DetalleVenta)
def descontar_stock_al_vender(sender, instance, created, **kwargs):
    """
    Resta stock cuando se agrega un producto al ticket.
    """
    if created:
        producto = instance.id_producto
        producto.stock_actual -= instance.cantidad
        producto.save()

# POST_DELETE
@receiver(post_delete, sender=DetalleVenta)
def corregir_stock_por_borrado_item(sender, instance, **kwargs):
    """
    Si se borra un renglón del ticket (antes de anular), devolvemos el stock.
    """
    producto = instance.id_producto
    producto.stock_actual += instance.cantidad
    producto.save()