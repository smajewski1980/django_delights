from django import forms

from .models import Ingredient, MenuItem, RecipeRequirement, Customer, Order


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = "__all__"


class AddIngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = "__all__"


class AddRecipeReq(forms.ModelForm):
    class Meta:
        model = RecipeRequirement
        fields = '__all__'
