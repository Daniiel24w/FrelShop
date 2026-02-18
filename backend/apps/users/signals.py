from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Usuario

@receiver(post_save, sender=Usuario)
def sincronizar_grupos_permisos(sender, instance, created, **kwargs):
    """
    Si el usuario tiene un 'rol' asignado, lo agregamos automáticamente 
    al ManyToMany 'groups' de Django para que herede sus permisos.
    """
    if instance.rol:
        if not instance.groups.filter(id=instance.rol.id).exists():
            instance.groups.clear() 
            instance.groups.add(instance.rol)

@receiver(pre_save, sender=Usuario)
def gestionar_baja_usuario(sender, instance, **kwargs):
    if instance.pk:
        usuario_db = Usuario.objects.get(pk=instance.pk)
        if not usuario_db.is_deleted and instance.is_deleted:
            instance.fh_baja = timezone.now()
            instance.is_active = False
        elif usuario_db.is_deleted and not instance.is_deleted:
            instance.fh_baja = None
            instance.is_active = True