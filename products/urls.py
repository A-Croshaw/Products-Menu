from django.urls import path
from . import views


urlpatterns = [
    path('', views.product_manager, name='product-manager'),
    path("products/", views.product_manager, name='product-list'),
]
