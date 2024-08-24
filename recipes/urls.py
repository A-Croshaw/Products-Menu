
from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipes_manager, name='recipe-manager'),
]
