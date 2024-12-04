from django.urls import path
from . import views

urlpatterns = [
    #----Recipe Manager
    path('', views.recipe_manager, name='recipe-manager'),
    path("recipes/", views.recipe_manager, name='recipe-list'),
    #----Recipe
    path('<pk>/view/', views.view_recipe, name='recipe-view'),
    path('add/', views.recipe_add, name='recipe-add'),
    path("<int:pk>/update/", views.recipe_update, name='recipe-update'),
    path('<int:pk>/delete/', views.recipe_delete, name='recipe-delete'),
    #----Recipe Ingredients
    path('<pk>/ingredients/', views.ingredients, name='ingredients'),
    path('details_ingredient/<pk>/', views.ingredient_details, name="ingredient-details"),
    path('update_ingredient/<pk>/', views.ingredient_update, name="ingredient-update"),
    path('delete_ingredient/<pk>/', views.ingredient_delete, name="ingredient-delete"),
    #----Recipe Method
    path('<pk>/method/', views.method, name='method'),
    path('details_method/<pk>/', views.method_details, name="method-details"),
    path('update_method/<pk>/', views.method_update, name="method-update"),
    path('delete_method/<pk>/', views.method_delete, name="method-delete"),
]
