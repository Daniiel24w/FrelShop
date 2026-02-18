from django.db import models
from django.conf import settings

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)

    cuit = models.CharField(max_length=20, unique=True, verbose_name="CUIT")
    razon_social = models.CharField(max_length=150, verbose_name="Razon Social")
    nombre_contacto = models.CharField(max_length=100, null=True, blank=True, verbose_name="Preventista")
    telefono = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)

    # Auditoria
    estado = models.BooleanField(default=True, verbose_name="Activo")
    id_usuario_alta = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='proveedores_creados')
    fh_alta = models.DateTimeField(auto_now_add=True)
    id_usuario_modificacion = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='proveedores_modificados')
    fh_modificacion = models.DateTimeField(auto_now=True)
    id_usuario_baja = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='proveedores_baja')
    fh_baja = models.DateTimeField(null=True, blank=True)

    # Clase meta
    class Meta:
        db_table = 'proveedores'
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

    def __str__(self):
        return f"{self.razon_social} (CUIT: {self.cuit})"