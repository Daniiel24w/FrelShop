from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Rutas Core
    path('', views.home, name='home'),
    
    # Rutas Boxes
    # path('cajas/'),
    
    # Rutas Customers
    # path('clientes/'),    
    
    # Rutas Products
    # path('productos/'),
    
    # Rutas Purcharses
    # path('compras/'),
    
    # Rutas Sales
    # path('ventas/'),
    
    # Rutas Suppliers
    # path('proveedores/'),
    
    # Rutas Users
    # path('usuarios/'),

]