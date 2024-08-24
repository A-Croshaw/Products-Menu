from django.contrib import admin
from .models import Recipe, Ingredients, Method, RecipeCategory


class RecipeCategoryAdmin(admin.ModelAdmin):
    """
    Creates Admin For The Category
    """
    fieldsets = []
    list_display = (
        'category',
    )
    ordering = ("category",)


class IngredientsAdminInline(admin.TabularInline):
    """
    Creates Admin For The Ingredients
    """
    model = Ingredients
    readonly_fields = ('ingredient_cost',)


class MethodAdminInline(admin.StackedInline):
    """
    reates Admin For The Method
    """
    model = Method
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    """
    Creates Admin For The Main Part OF The Recipe And Adds Method
    And Ingredients To an Inline Output and Displays as one Item
    """
    fieldsets = []
    inlines = (IngredientsAdminInline, MethodAdminInline)
    list_filter = ("category", "recipe",)
    ordering = ("category", "recipe",)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredients)
admin.site.register(Method)
admin.site.register(RecipeCategory, RecipeCategoryAdmin)
