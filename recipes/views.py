from django.http.response import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.decorators import (
    login_required, permission_required)
from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower



def recipes_manager(request):
    """
    A view to render recipe manager
    """

    template = 'recipes/recipe-manager.html'
    return render(request, template,)
