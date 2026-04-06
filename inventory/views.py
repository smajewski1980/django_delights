from django.shortcuts import render
from django.views.generic.list import ListView
from inventory.models import Ingredient, Order, MenuItem, RecipeRequirement

# Create your views here.


class CurrentInventory(ListView):
    model = Ingredient
    context_object_name = 'currInventory'
    template_name = 'inventory/inventory.html'


def index(request):
    return render(request, 'inventory/index.html')


class Purchases(ListView):
    model = Order
    context_object_name = 'purchases'
    template_name = 'inventory/purchases.html'


class Menu(ListView):
    model = MenuItem
    context_object_name = 'menu_items'
    template_name = 'inventory/menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # how to access foreign key data
        context["recipe_reqs"] = RecipeRequirement.objects.all()
        return context
