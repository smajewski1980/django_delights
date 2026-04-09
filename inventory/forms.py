from django import forms

from .models import Ingredient, MenuItem, RecipeRequirement, Customer, Order


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = "__all__"
