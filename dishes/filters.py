import django_filters
from dishes.models import Dishes, DishCategory


class DishesFilter(django_filters.FilterSet):
    catergory = django_filters.ModelChoiceFilter(
        queryset=DishCategory.objects.all(),
        field_name="category",
        lookup_expr="exact",
        empty_label="Any",
    )

    class Meta:
        model = Dishes
        fields = ('category', 'subcategory',)