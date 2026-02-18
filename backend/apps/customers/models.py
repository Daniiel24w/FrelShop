from django.db import models

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True) 
    
    cuil = models.CharField(max_length=20, unique=True, null=True, blank=True) 
    nombre = models.CharField(max_length=100) 
    apellido = models.CharField(max_length=100)    
    telefono = models.CharField(max_length=20, null=True, blank=True) 
    email = models.EmailField(null=True, blank=True) 
    direccion = models.CharField(max_length=255, null=True, blank=True, verbose_name="Dirección")
    
    # Auditoria
    estado = models.BooleanField(default=True, help_text="Indica si el cliente está activo para realizar ventas")
    fh_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Alta")

    class Meta:
        db_table = 'clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes' 

    def __str__(self):
        return f"{self.apellido}, {self.nombre} (CUIL: {self.cuil})"