from django.contrib import admin
from .models import Product, Category, Subcategory


class ProductAdmin(admin.ModelAdmin):
    """
    Creates Admin For The Products
    """
    fieldsets = []

    list_display = (
        "product",
        "category",
        "subcategory",
        "cost",
        "quantity",
        "unit"
    )

    list_filter = ('product',"category", "subcategory", "cost",)
    ordering = ("product","category", "subcategory",)


class CategoryAdmin(admin.ModelAdmin):
    """
    Creates Admin For The Category
    """
    fieldsets = []
    list_display = (
        'category',
    )
    ordering = ("category",)


class SubcategoryAdmin(admin.ModelAdmin):
    """
    Creates Admin For The Subcategory
    """
    fieldsets = []
    list_display = (
        'subcategory',
    )
    ordering = ( "subcategory",)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
