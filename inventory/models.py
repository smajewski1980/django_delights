from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=200)
    ingredient_inv_qty = models.FloatField(validators=[MinValueValidator(0)])
    ingredient_unit = models.CharField(max_length=200)
    ingredient_unit_price = models.FloatField(
        validators=[MinValueValidator(0)])

    def __str__(self):
        return self.ingredient_name


class MenuItem(models.Model):
    menu_item_name = models.CharField(max_length=200)
    menu_item_price = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.menu_item_name


class RecipeRequirement(models.Model):
    recipe_qty = models.FloatField(validators=[MinValueValidator(0)])
    ingredient_name = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    menu_item_name = models.ForeignKey(MenuItem, on_delete=models.CASCADE)


class Customer(models.Model):
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()

    def __str__(self):
        return self.customer_name


class Order(models.Model):
    order_timestamp = models.DateTimeField(auto_now=True)
    customer_name = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_total = models.FloatField(validators=[MinValueValidator(0)])
    menu_item_name = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
