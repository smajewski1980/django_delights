from django.shortcuts import render
from django.views.generic.list import ListView
from inventory.models import Ingredient

# Create your views here.


class CurrentInventory(ListView):
    model = Ingredient
    template_name = 'inventory/inventory.html'
