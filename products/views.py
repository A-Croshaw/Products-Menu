from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.contrib.auth.decorators import (
    login_required, permission_required)
from django.db.models import Q
from django.contrib import messages
from django_htmx.http import retarget
from products.filters import ProductFilter
from .models import Product
from .forms import ProductForm


@login_required
def product_manager(request):
    """ Render Products Manager """

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
        template ='products/includes/product-list-container.html'
        return render(request, template, context)

    template= 'products/product-manager.html'
    return render(request, template, context)


@login_required
@permission_required("products.product_add", raise_exception=True)
def product_add(request):
    """ Add A Product Function, (admin users only) """

    if not request.user.is_superuser:
        messages.error(request, 'Admin users can only add products.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            context = {'message': f'{product.product} was successfully added'}
            template = 'products/includes/product-success.html'
            return render(request, template, context)
        else:
            context = {'form': form}
            template = 'products/includes/product-add.html'
            response = render(request, template, context)
            return retarget(response, '#product-add')

    template = 'products/includes/product-add.html'
    context = {
        'form': ProductForm(),
    }
    return render(request, template, context)


@login_required
@permission_required("products.product_update", raise_exception=True)
def product_update(request, pk):
    """ Update A Product Function (admin users only) """

    if not request.user.is_superuser:
        messages.error(request, 'Admin users only can edit products.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product=form.save()
            context = {'message': f'{product.product} was successfully updated!'}
            template = 'products/includes/product-success.html'
            return render(request, template, context)
        else:
            context = {
                'form': form,
                'product': product,
            }
            template = 'products/includes/product-update.html'
            response = render(request, template, context)
            return retarget(response, '#product-add')

    template = 'products/includes/product-update.html'
    context = {
        'form': ProductForm(instance=product),
        'product': product,
    }

    return render(request, template, context)


@login_required
@permission_required("products.product_delete", raise_exception=True)
def product_delete(request, pk):
    """ Delete Products Function (admin users only) """

    if not request.user.is_superuser:
        messages.error(request, 'Admin users can only delete products.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=pk,)
    product.delete()

    template = 'products/includes/product-success.html'
    context = {
        'message': 
        f"Product: {product.product} {product.quantity}{product.unit} was deleted successfully!"
    }

    return render(request, template, context)
