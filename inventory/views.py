from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView, FormView, UpdateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from inventory.models import Ingredient, Order, MenuItem, RecipeRequirement
from .forms import MenuItemForm, AddIngredientForm, AddRecipeReq, AddNewOrder

# Create your views here.


class login_view(auth_views.LoginView):
    template_name = 'inventory/login.html'
    next_page = '/purchases/'


class logout_view(auth_views.LogoutView):
    next_page = 'home'


class CurrentInventory(LoginRequiredMixin, ListView):
    model = Ingredient
    context_object_name = 'currInventory'
    template_name = 'inventory/inventory.html'
    login_url = '/login/'
    title = 'Inventory-Django Delights'

    def get_title(self):
        return self.title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_title()

        return context


def index(request):
    return render(request, 'inventory/index.html')


class Purchases(LoginRequiredMixin, ListView):
    model = Order
    context_object_name = 'purchases'
    template_name = 'inventory/purchases.html'
    title = 'Orders-Django Delights'
    login_url = '/login/'

    def get_title(self):
        return self.title

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
        context['title'] = self.get_title()
        print(self.request.user)
        return context


class Menu(LoginRequiredMixin, ListView):
    model = MenuItem
    context_object_name = 'menu_items'
    template_name = 'inventory/menu.html'
    login_url = '/login/'
    title = 'Menu-Django Delights'

    def get_title(self):
        return self.title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_items = self.get_queryset()
        recipe_requirements = {}

        for item in menu_items:
            recipe_requirements[item.menu_item_name] = RecipeRequirement.objects.filter(
                menu_item_name=item)

        context["recipe_reqs"] = recipe_requirements
        context['title'] = self.get_title()
        return context


# dont know yet if this is correct
class DeleteIngredient(LoginRequiredMixin, DeleteView):
    model = Ingredient
    template_name = 'inventory/delete.html'
    success_url = 'inventory/'
    login_url = '/login/'


class NewMenuItem(LoginRequiredMixin, FormView):
    template_name = 'inventory/new_menu_item.html'
    form_class = MenuItemForm
    success_url = '/menu/'
    login_url = '/login/'
    title = 'New Menu Item-Django Delights'

    def get_title(self):
        return self.title

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_title()
        return context


class NewIngredient(LoginRequiredMixin, FormView):
    template_name = 'inventory/new_ingredient.html'
    form_class = AddIngredientForm
    success_url = '/inventory/'
    login_url = '/login/'
    title = 'New Ingredient-Django Delights'

    def get_title(self):
        return self.title

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_title()

        return context


class NewRecipeReq(LoginRequiredMixin, FormView):
    template_name = 'inventory/new_recipe_req.html'
    form_class = AddRecipeReq
    success_url = '/new_recipe_req/'
    login_url = '/login/'
    title = 'New Recipe Req-Django Delights'

    def get_title(self):
        return self.title

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_title()
        return context


class NewOrder(LoginRequiredMixin, FormView):
    template_name = 'inventory/new_order.html'
    form_class = AddNewOrder
    success_url = '/purchases/'
    login_url = '/login/'
    title = 'New Order-Django Delights'

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
            if curr_inv_qty and int(ingr[1]) > int(curr_inv_qty[0]):
                not_enough.append(ingr[0])
        # if not enough has any items, go through and return errors with the invalid form
        if not len(not_enough):
            form.save()
            for item in rec_reqs:
                # self.update_the_inv(item)
                name = item[0]
                qty = item[1]
                ingredient = Ingredient.objects.get(ingredient_name=name)
                if ingredient.ingredient_inv_qty >= qty:
                    ingredient.ingredient_inv_qty -= qty
                    ingredient.save()
                else:
                    print(f'not enough {item} in inventory')
                    form.add_error(
                        'menu_item_name', f'not enough {item[0]} in inventory')
                    return self.form_invalid(form)
            return super().form_valid(form)
        else:
            for item in not_enough:
                form.add_error(
                    'menu_item_name', f'not enough {item} in inventory')
            return self.form_invalid(form)

    def get_title(self):
        return self.title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["item_prices"] = list(MenuItem.objects.order_by(
            'id').values_list('menu_item_price', flat=True))
        context['title'] = self.get_title()

        return context


class UpdateInventory(LoginRequiredMixin, UpdateView):
    model = Ingredient
    fields = '__all__'
    template_name = 'inventory/update_inventory.html'
    success_url = '/inventory/'
    login_url = '/login/'
