from django.urls import path
from .views import ProductManager


urlpatterns = [
    path('',ProductManager.as_view(), name='product-manager'),
]
