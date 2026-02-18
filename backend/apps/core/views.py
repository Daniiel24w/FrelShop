from django.shortcuts import render

# Imports models
from apps.boxes.models import Caja, MovimientoCaja
from apps.customers.models import Cliente
from apps.products.models import Categoria, Marca, UnidadMedida, Producto, Promocion
from apps.purchases.models import Compra, DetalleCompra
from apps.sales.models import Venta, DetalleVenta
from apps.suppliers.models import Proveedor
from apps.users.models import Usuario

def home(request):
    """
    Vista principal que renderiza el dashboard o home.
    """
    context = {
        'titulo': 'Dashboard Principal',
        'mensaje': 'Bienvenido al Sistema de Gestión Centralizado'
    }
    return render(request, 'core/index.html', context)