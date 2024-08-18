##from django.shortcuts import render


from django.views.generic import TemplateView

class ProductManager(TemplateView):

    template_name = 'products/product-manager.html'
