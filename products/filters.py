import django_filters
from products.models import Product, Category, Subcategory



class ProductFilter(django_filters.FilterSet):
    catergory = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        field_name="category",
        lookup_expr="exact",
        empty_label="Any",
    )

    subcatergory = django_filters.ModelChoiceFilter(
        queryset=Subcategory.objects.all(),
        field_name="subcategory",
        lookup_expr="exact",
        empty_label="Any",
    )

    class Meta:
        model = Product
        fields = ('category', 'subcategory',)

