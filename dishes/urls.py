from django.urls import path
from . import views


urlpatterns = [
    path("", views.dish_manager, name='dish-manager'),
    path("dishes/", views.dish_manager, name='dish-list'),
]