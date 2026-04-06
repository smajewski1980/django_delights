from django.shortcuts import render
from django.views.generic.list import ListView
from inventory.models import Ingredient, Order

# Create your views here.


class CurrentInventory(ListView):
    model = Ingredient
    template_name = 'inventory/inventory.html'


def index(request):
    return render(request, 'inventory/index.html')


class Purchases(ListView):
    model = Order
    template_name = 'inventory/purchases.html'
