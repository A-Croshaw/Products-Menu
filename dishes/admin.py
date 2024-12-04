from django.contrib import admin
from .models import Dishes, DishSauce, DishSides, DishElement, DishCategory


class DishCategoryAdmin(admin.ModelAdmin):
    """
    Creates Admin For The Category
    """
    fieldsets = []
    list_display = (
        'category',
    )
    ordering = ("category",)


class DishSauceAdminInline(admin.TabularInline):
    """
    Creates Admin For The Sauce
    """
    model = DishSauce
    readonly_fields = ('sauce_cost',)


class DishElementAdminInline(admin.TabularInline):
    """
    Creates Admin For The Dish Elements
    """
    model = DishElement
    readonly_fields = ('element_cost',)


class DishSidesAdminInline(admin.TabularInline):
    """
    Creates Admin For The Dish Sides
    """
    model = DishSides
    readonly_fields = ('side_cost',)


class DishesAdmin(admin.ModelAdmin):
    """
    Creates Admin For The Main Part OF The Dishes And Adds Method
    And Ingredients To an Inline Output and Displays as one Item
    """
    fieldsets = []
    inlines = (DishSauceAdminInline, DishElementAdminInline, DishSidesAdminInline)
    list_filter = ("category", "dish_name",)
    ordering = ("category", "dish_name",)


admin.site.register(Dishes, DishesAdmin)
admin.site.register(DishSauce)
admin.site.register(DishElement)
admin.site.register(DishSides)
admin.site.register(DishCategory, DishCategoryAdmin)
