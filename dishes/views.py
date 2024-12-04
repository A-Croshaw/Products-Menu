from django.http.response import HttpResponse, HttpResponseNotAllowed
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.contrib.auth.decorators import (
    login_required, permission_required)
from django.db.models import Q
from django.contrib import messages
from django_htmx.http import retarget
from dishes.filters import DishesFilter
from .models import Dishes


# ------------------------------------------------------------------ Dish Manager
@login_required
def dish_manager(request):
    """ Render Dish Manager """

    dishes=Dishes.objects.all()
    dishes_filter = None
    query = None
    if 'q' in request.GET:
        query = request.GET['q']
        queries = Q(dish_name__icontains=query)
        dishes= dishes.filter(queries)
        dishes_filter = DishesFilter(
            request.GET,dishes
            )
    else:
        dishes_filter = DishesFilter(
            request.GET,
            )

    context = {
        'filter': dishes_filter,
        'dishes':dishes,
        }

    if request.htmx:
        template ='dishes/includes/dish-list-container.html'
        return render(request, template, context)

    template= 'dishes/dish-manager.html'
    return render(request, template, context)