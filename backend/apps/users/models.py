from django.db import models
from django.contrib.auth.models import AbstractUser, Group

# ROLES [ ESTA PARTE LA COMENTO POR QUE ERA UNA TABLA PERO LUEGO OPTE POR UTILIZAR LOS GRUPOS DE DJANGO E INTEGRARLOS EN LA CLASE USUARIO ]
# class Rol(models.Model):
#     id_rol = models.AutoField(primary_key=True)
#     nombre = models.CharField(max_length=50, unique=True)
#     descripcion = models.TextField(null=True, blank=True)    
#     class Meta:
#         db_table = 'roles'
#         verbose_name = 'Rol'
#         verbose_name_plural = 'Roles'
#     def __str__(self):
#         return self.nombre

class Usuario(AbstractUser):
    id_usuario = models.AutoField(primary_key=True)
    rol = models.ForeignKey(Group, on_delete=models.PROTECT, null=True, blank=True,verbose_name="Rol del Sistema",related_name="usuarios_con_este_rol")

    dni = models.CharField(max_length=20, unique=True, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    avatar_url = models.ImageField(upload_to='avatars/', null=True, blank=True)


    # Auditoria
    fh_alta = models.DateTimeField(auto_now_add=True)
    fh_modificacion = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    fh_baja = models.DateTimeField(null=True, blank=True)
    
    # Herencia de Django
    groups = models.ManyToManyField('auth.Group',related_name='usuarios_custom_user_groups',blank=True)
    user_permissions = models.ManyToManyField('auth.Permission',related_name='usuarios_custom_user_permissions',blank=True)

    # Clase meta 
    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        rol_nombre = self.rol.name if self.rol else 'Sin Rol'
        return f"{self.username} ({rol_nombre})"
