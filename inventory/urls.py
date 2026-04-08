from django.urls import path
from inventory import views

urlpatterns = [
    path('', views.index, name='home'),
    path('inventory/', views.CurrentInventory.as_view(), name='inventory'),
    path('purchases/', views.Purchases.as_view(), name='purchases'),
    path('menu', views.Menu.as_view(), name='menu')
]
