from django.contrib import admin

# Register your models here.
from .models import Ingredient, MenuItem, RecipeRequirement, Customer, Order

admin.site.register(Ingredient)
admin.site.register(MenuItem)
admin.site.register(RecipeRequirement)
admin.site.register(Customer)
admin.site.register(Order)
