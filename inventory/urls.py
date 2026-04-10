from django.urls import path
from inventory import views

urlpatterns = [
    path('', views.index, name='home'),
    path('inventory/', views.CurrentInventory.as_view(), name='inventory'),
    path('purchases/', views.Purchases.as_view(), name='purchases'),
    path('menu/', views.Menu.as_view(), name='menu'),
    path('new_menu_item/', views.NewMenuItem.as_view(), name='new_menu_item'),
    path('new_ingredient/', views.NewIngredient.as_view(), name='new_ingredient'),
    path('new_recipe_req/', views.NewRecipeReq.as_view(), name='new_recipe_req'),
    path('new_order/', views.NewOrder.as_view(), name='new_order'),
    path('inventory/<int:pk>/',
         views.UpdateInventory.as_view(), name='update_inventory')
]
