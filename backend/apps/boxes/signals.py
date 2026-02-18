from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import MovimientoCaja, Caja

# PRE_SAVE
@receiver(pre_save, sender=MovimientoCaja)
def ajustar_monto_por_edicion(sender, instance, **kwargs):
    """
    Si se edita el monto de un movimiento existente, 
    ajustamos la caja con la diferencia.
    """
    if instance.pk: 
        movimiento_viejo = MovimientoCaja.objects.get(pk=instance.pk)
        caja = instance.id_caja
        
        diferencia = instance.monto - movimiento_viejo.monto
        
        if instance.tipo_movimiento == 'INGRESO':
            caja.monto_final_sistema += diferencia
        elif instance.tipo_movimiento == 'EGRESO':
            caja.monto_final_sistema -= diferencia
            
        caja.save()

@receiver(pre_save, sender=MovimientoCaja)
def validar_caja_abierta(sender, instance, **kwargs):
    """
    Impide crear o modificar movimientos en una caja que ya fue cerrada.
    """
    if not instance.id_caja.estado:
        raise ValidationError(
            f"No se pueden registrar movimientos en la Caja #{instance.id_caja.pk} porque ya está cerrada."
        )

# POST_DELETE
@receiver(post_delete, sender=MovimientoCaja)
def revertir_monto_sistema(sender, instance, **kwargs):
    """
    Si un movimiento se elimina, restamos (o sumamos) el monto 
    de la caja para mantener el saldo real.
    """
    caja = instance.id_caja
    if instance.tipo_movimiento == 'INGRESO':
        caja.monto_final_sistema -= instance.monto
    elif instance.tipo_movimiento == 'EGRESO':
        caja.monto_final_sistema += instance.monto
    
    caja.save()

# POST_SAVE
@receiver(post_save, sender=MovimientoCaja)
def actualizar_monto_sistema(sender, instance, created, **kwargs):
    """
    Cada vez que se registra un movimiento, actualizamos el 
    monto_final_sistema de la caja asociada.
    """
    if created:
        caja = instance.id_caja
        
        if instance.tipo_movimiento == 'INGRESO':
            caja.monto_final_sistema += instance.monto
        elif instance.tipo_movimiento == 'EGRESO':
            caja.monto_final_sistema -= instance.monto
        caja.save()

@receiver(post_save, sender=Caja)
def calcular_diferencia_cierre(sender, instance, created, **kwargs):
    if not created:
        if instance.estado == False and instance.monto_final_real is not None:
            nueva_diferencia = instance.monto_final_real - instance.monto_final_sistema
            
            Caja.objects.filter(pk=instance.pk).update(monto_diferencia=nueva_diferencia)