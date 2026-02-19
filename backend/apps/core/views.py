from django.shortcuts import render

# Imports models
from apps.boxes.models import Caja, MovimientoCaja
from apps.customers.models import Cliente
from apps.products.models import Categoria, Marca, UnidadMedida, Producto, Promocion
from apps.purchases.models import Compra, DetalleCompra
from apps.sales.models import Venta, DetalleVenta
from apps.suppliers.models import Proveedor
from apps.users.models import Usuario


# VISTAS
    # CORE
def home(request):
    return render(request, 'core/index.html')

    # CAJA
def boxOpening(request):
    return render(request, 'core/apps/boxes/BoxOpening.html')

def boxClosing(request):
    return render(request, 'core/apps/boxes/BoxClosing.html')

def boxStatus(request):
    return render(request, 'core/apps/boxes/BoxStatus.html')

    # CLIENTES
def customer(request):
    return render(request, 'core/apps/customers/Customers.html')

    # PROVEEDORES
def supplier(request):
    return render(request, 'core/apps/suppliers/Suppliers.html')

    # COMPRAS
def purchaseOrder(request):
    return render(request, 'core/apps/purchases/PurchasesOrder.html')

def purchaseReport(request):
    return render(request, 'core/apps/purchases/PurchasesReport.html')

    # VENTAS
def salesNew(request):
    return render(request, 'core/apps/sales/SalesNew.html')

def salesHistory(request):
    return render(request, 'core/apps/sales/SalesHistory.html')

def salesReport(request):
    return render(request, 'core/apps/sales/SalesReport.html')
    
    # USUARIO
def userProfile(request):
    return render(request, 'core/apps/users/UserProfile.html')

def userProfileEdit(request):
    return render(request, 'core/apps/users/UserProfileEdit.html')

    # PRODUCTOS
def product(request):
    return render(request, 'core/apps/products/Products.html')

def productReport(request):
    return render(request, 'core/apps/products/ProductsReport.html')