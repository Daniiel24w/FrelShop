from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Producto

# PRE_SAVE''
@receiver(pre_save, sender=Producto)
def validar_precio_y_stock(sender, instance, **kwargs):
    if instance.stock_actual < 0:
        instance.stock_actual = 0 
        
    if instance.precio_venta < 0:
        instance.precio_venta = 0

@receiver(pre_save, sender=Producto)
def verificar_margen_ganancia(sender, instance, **kwargs):
    if instance.precio_venta <= instance.precio_compra:
        print(f"AVISO: El producto {instance.nombre} tiene un margen de ganancia nulo o negativo.")

# POST_SAVE''
@receiver(post_save, sender=Producto)
def alertar_stock_bajo(sender, instance, **kwargs):
    if instance.stock_actual <= instance.stock_minimo:
        print(f"ALERTA: El producto {instance.nombre} está por debajo del stock mínimo.")