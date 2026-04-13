from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView, FormView, UpdateView
from inventory.models import Ingredient, Order, MenuItem, RecipeRequirement
from .forms import MenuItemForm, AddIngredientForm, AddRecipeReq, AddNewOrder

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_totals = self.get_queryset()
        sum_totals = sum([item.order_total for item in order_totals])
        context['total_orders_sum'] = sum_totals

        orders = self.get_queryset()
        ordered_items = [item.menu_item_name for item in orders]
        recipe_requirements = RecipeRequirement.objects.all()
        list_of_ingr_for_calc = []
        cost = 0

        for item in ordered_items:
            for ingr in recipe_requirements:
                if ingr.menu_item_name == item:
                    list_of_ingr_for_calc.append(
                        (ingr.ingredient_name, ingr.recipe_qty))

        for ingr in list_of_ingr_for_calc:
            ingr_name = ingr[0]
            ingr_qty_used = ingr[1]
            currIngr = Ingredient.objects.filter(ingredient_name=ingr_name)[0]
            cost += currIngr.ingredient_unit_price * ingr_qty_used

        context['ingr_used_cost'] = cost
        context['profit'] = sum_totals - cost
        context['purchases'] = context['purchases'][::-1]

        return context


class Menu(ListView):
    model = MenuItem
    context_object_name = 'menu_items'
    template_name = 'inventory/menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_items = self.get_queryset()
        recipe_requirements = {}

        for item in menu_items:
            recipe_requirements[item.menu_item_name] = RecipeRequirement.objects.filter(
                menu_item_name=item)

        context["recipe_reqs"] = recipe_requirements
        return context


# dont know yet if this is correct
class DeleteIngredient(DeleteView):
    model = Ingredient
    template_name = 'inventory/delete.html'
    success_url = 'inventory/'


class NewMenuItem(FormView):
    template_name = 'inventory/new_menu_item.html'
    form_class = MenuItemForm
    success_url = '/menu/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class NewIngredient(FormView):
    template_name = 'inventory/new_ingredient.html'
    form_class = AddIngredientForm
    success_url = '/inventory/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class NewRecipeReq(FormView):
    template_name = 'inventory/new_recipe_req.html'
    form_class = AddRecipeReq
    success_url = '/new_recipe_req/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class NewOrder(FormView):
    template_name = 'inventory/new_order.html'
    form_class = AddNewOrder
    success_url = '/purchases/'

    def form_valid(self, form):
        '''check to see if the desired menu item has enough ingredients in inventory'''
        menu_item_name = form.cleaned_data['menu_item_name']
        # the ingredients for this menu item
        rec_reqs = []
        # this holds the items that have insufficient inventory if they exist
        not_enough = []
        # get the ingredients required
        for row in RecipeRequirement.objects.all():
            if row.menu_item_name == menu_item_name:
                rec_reqs.append((row.ingredient_name, row.recipe_qty))
        # check if ingredients have enough in inventory
        for ingr in rec_reqs:
            ingredients = Ingredient.objects.all()
            curr_inv_qty = [
                item.ingredient_inv_qty for item in ingredients if str(item.ingredient_name) == str(ingr[0])]
            # if not add to not enoughj list
            if int(ingr[1]) > int(curr_inv_qty[0]):
                not_enough.append(ingr[0])
        # if not enough has any items, go through and return errors with the invalid form
        if not len(not_enough):
            form.save()
            return super().form_valid(form)
        else:
            for item in not_enough:
                form.add_error(
                    'menu_item_name', f'not enough {item} in inventory')
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["item_prices"] = list(MenuItem.objects.order_by(
            'id').values_list('menu_item_price', flat=True))

        return context


class UpdateInventory(UpdateView):
    model = Ingredient
    fields = '__all__'
    template_name = 'inventory/update_inventory.html'
    success_url = '/inventory/'
