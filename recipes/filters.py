import django_filters
from recipes.models import Recipe, RecipeCategory


class RecipeFilter(django_filters.FilterSet):
    catergory = django_filters.ModelChoiceFilter(
        queryset=RecipeCategory.objects.all(),
        field_name="category",
        lookup_expr="exact",
        empty_label="Any",
    )

    class Meta:
        model = Recipe
        fields = ('category', 'subcategory',)