from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.db.models import Q
from products.filters import ProductFilter
from .models import Product


def product_manager(request):
    """
    A view to render products manager
    """
    products=Product.objects.all()
    product_filter = None
    query = None
    if 'q' in request.GET:
        query = request.GET['q']
        queries = Q(product__icontains=query)
        products= products.filter(queries)
        product_filter = ProductFilter(
            request.GET,products
            )
    else:
        product_filter = ProductFilter(
            request.GET,
            )


    context = {
        'filter': product_filter,
        'product':products,
        }

    if request.htmx:
        return render(request, 'products/includes/product-list-container.html', context)

    return render(request, 'products/product-manager.html', context)
