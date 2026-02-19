from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Rutas Core
    path('', views.home, name='home'),
    
    # Rutas Boxes
    path('caja/apertura/', views.boxOpening, name='boxOpening'),
    path('caja/cierre/', views.boxClosing, name='boxClosing'),
    path('caja/estado/', views.boxStatus, name='boxStatus'),
    
    # Rutas Customers
    path('cliente/', views.customer, name='customer'),   
    
    # Rutas Products
    path('productos/', views.product, name='product'),
    path('productos/reportes', views.productReport, name='productReport'),
    
    # Rutas Purcharses
    path('compras/', views.purchaseOrder, name='purchaseOrder'),
    path('compras/reportes/', views.purchaseReport, name='purchaseReport'),
    
    # Rutas Sales
    path('venta/nueva/', views.salesNew, name='salesNew'),
    path('venta/historial/', views.salesHistory, name='salesHistory'),
    path('venta/reportes/', views.salesReport, name='salesReport'),
    
    # Rutas Suppliers
    path('proveedores/', views.supplier, name='supplier'),

    # Rutas Users
    path('usuario/profile/', views.userProfile, name='userProfile'),
    path('usuario/profile/edit', views.userProfileEdit, name='userProfileEdit'),

]