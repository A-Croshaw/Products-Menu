from django.http.response import HttpResponse, HttpResponseNotAllowed
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.contrib.auth.decorators import (
    login_required, permission_required)
from django.db.models import Q
from django.contrib import messages
from django_htmx.http import retarget
from recipes.filters import RecipeFilter
from .models import Recipe, Method, Ingredients
from .forms import RecipeForm, MethodForm, IngredientsForm


# ------------------------------------------------------------------ Recipe Manager
@login_required
def recipe_manager(request):
    """ Render recipes Manager """

    recipes=Recipe.objects.all()
    recipe_filter = None
    query = None
    if 'q' in request.GET:
        query = request.GET['q']
        queries = Q(recipe_name__icontains=query)
        recipes= recipes.filter(queries)
        recipe_filter = RecipeFilter(
            request.GET,recipes
            )
    else:
        recipe_filter = RecipeFilter(
            request.GET,
            )

    context = {
        'filter': recipe_filter,
        'recipe':recipes,
        }

    if request.htmx:
        template ='recipes/includes/recipe-list-container.html'
        return render(request, template, context)

    template= 'recipes/recipe-manager.html'
    return render(request, template, context)


# ------------------------------------------------------------------ View Recipe
def view_recipe(request, pk):
    """View full Recipie"""
    recipe = Recipe.objects.get(id=pk)
    step = Method.objects.filter(recipe=recipe)
    ingredient = Ingredients.objects.filter(recipe=recipe)

    template = "recipes/recipe-view.html"
    context = {
        "recipe": recipe,
        "step": step,
        "ingredient": ingredient
    }
    return render(request, template, context,)


# ------------------------------------------------------------------ Add Recipe
@login_required
@permission_required("recipes.add_recipe", raise_exception=True)
def recipe_add(request):
    """
    Add Recipe function
    """
    if not request.user.is_superuser:
        messages.error(request, 'Admin users can only add recipes.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe= form.save()
            template = 'recipes/recipe-ingredients.html'
            context ={'recipe': recipe}
            return render(request, template, context)
        else:
            context = {'form': form}
            template = 'recipes/recipe-add.html'
            response = render(request, template)
            return retarget(response, '#recipe-add')

    template = 'recipes/recipe-add.html'
    context = {
        'form': RecipeForm(),
    }
    return render(request, template, context)


# ------------------------------------------------------------------ Update Recipe
@login_required
@permission_required("recipes.recipe_update", raise_exception=True)
def recipe_update(request, pk):
    """ Update A Recipe Function (admin users only) """

    if not request.user.is_superuser:
        messages.error(request, 'Admin users only can edit recipes.')
        return redirect(reverse('home'))

    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            recipe=form.save()
            ingredient = Ingredients.objects.filter(recipe=recipe)
            template = 'recipes/recipe-ingredients.html'
            context ={'recipe': recipe,
                      'ingredient':ingredient}
            return render(request, template, context)
        else:
            context = {
                'form': form,
                'recipe': recipe,
            }
            template = 'recipes/recipe-update.html'
            response = render(request, template, context)
            return retarget(response, '#recipe-add')

    template = 'recipes/recipe-update.html'
    context = {
        'form': RecipeForm(instance=recipe),
        'recipe': recipe,
    }

    return render(request, template, context)


# ------------------------------------------------------------------ Delete Recipe
@login_required
@permission_required("recipes.recipe_delete", raise_exception=True)
def recipe_delete(request, pk):
    """ Delete Recipes Function (admin users only) """

    if not request.user.is_superuser:
        messages.error(request, 'Admin users can only delete recipes.')
        return redirect(reverse('home'))

    recipe = get_object_or_404(Recipe, pk=pk,)
    recipe.delete()

    template = 'recipes/recipe-success.html'
    context = {
        'message': 
        f"Recipe: {recipe.recipe_name} was deleted successfully!"
    }

    return render(request, template, context)


# ------------------------------------------------------------------ Ingredients
@login_required
@permission_required("recipes.ingredients", raise_exception=True)
def ingredients(request, pk):
    """Creates Ingredient Fields And Add More Enterys"""
    recipe = Recipe.objects.get(id=pk)
    ingredient = Ingredients.objects.filter(recipe=recipe)
    form = IngredientsForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.recipe = recipe
            ingredient.save()
            ingredient = Ingredients.objects.filter(recipe=recipe)
            template = 'recipes/recipe-ingredients.html'
            context ={"recipe": recipe,
                      "ingredient": ingredient,}
            response = render(request, template, context)
            return retarget(response, '#recipe-add')

    template = "recipes/recipe-ingredients.html"
    context = {
        "form": form,
        "recipe": recipe,
        "ingredient": ingredient,
    }
    return render(request, template, context)


# ------------------------------------------------------------------ Ingredients Details
def ingredient_details(request, pk):
    """Displays Ingredient Fields After Being Added"""
    ingredient = get_object_or_404(Ingredients, id=pk)
    template = "recipes/includes/ingredient-details.html"
    context = {
        "ingredient": ingredient
    }
    return render(request, template, context)


# ------------------------------------------------------------------ Update Ingredients
@login_required
@permission_required("recipes.ingredient_update", raise_exception=True)
def ingredient_update(request, pk):
    """Updates Ingredient Fields"""
    ingredient = Ingredients.objects.get(id=pk)
    form = IngredientsForm(
        request.POST or None,
        instance=ingredient
    )

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated Successfull!')
        return redirect("ingredient-details", pk=ingredient.id)

    template = "recipes/includes/ingredient-update.html"
    context = {
        "form": form,
        "ingredient": ingredient
    }
    return render(request, template, context)


# ------------------------------------------------------------------ Delete Ingredients
@login_required
@permission_required("recipes.ingredient_delete", raise_exception=True)
def ingredient_delete(request, pk):
    """Deletes Ingredient Fields"""
    ingredient = get_object_or_404(Ingredients, id=pk)

    if request.method == "POST":
        ingredient.delete()
        messages.success(request, 'Ingredient Deleted')
        return HttpResponse("")

    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )


# ------------------------------------------------------------------ Method
@login_required
@permission_required("recipes.method", raise_exception=True)
def method(request, pk):
    """Creates Method Fields And Add More Enterys"""
    recipe = Recipe.objects.get(id=pk)
    step = Method.objects.filter(recipe=recipe)
    form = MethodForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            step = form.save(commit=False)
            step.recipe = recipe
            step.save()
            step = Method.objects.filter(recipe=recipe)
            template = 'recipes/recipe-method.html'
            context ={"recipe": recipe,
                      "step": step,}
            response = render(request, template, context)
            return retarget(response, '#recipe-add')

    template = "recipes/recipe-method.html"
    context = {
        "form": form,
        "recipe": recipe,
        "step": step,
    }
    return render(request, template, context)


# ------------------------------------------------------------------ Method Details
def method_details(request, pk):
    """Displays Ingredient Fields After Being Added"""
    step = get_object_or_404(Method, id=pk)
    template = "recipes/includes/method-details.html"
    context = {
        "step": step
    }
    return render(request, template, context)


# ------------------------------------------------------------------ Update Method
@login_required
@permission_required("recipes.method_update", raise_exception=True)
def method_update(request, pk):
    """Updates Method Fields"""
    step = Method.objects.get(id=pk)
    form = MethodForm(
        request.POST or None,
        instance=step
    )

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated Successfull!')
        return redirect("method-details", pk=step.id)

    template = "recipes/includes/method-update.html"
    context = {
        "form": form,
        "step": step
    }
    return render(request, template, context)


# ------------------------------------------------------------------ Delete Method
@login_required
@permission_required("recipes.method_delete", raise_exception=True)
def method_delete(request, pk):
    """Deletes Method Fields"""
    step= get_object_or_404(Method, id=pk)

    if request.method == "POST":
        step.delete()
        messages.success(request, 'Method Deleted')
        return HttpResponse("")

    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )