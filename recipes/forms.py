from django import forms
from .models import Recipe, Ingredients, Method, RecipeCategory


class IngredientsForm(forms.ModelForm):
    """Ingredient Form"""

    class Meta:
        """
        Form Fields
        """
        model = Ingredients
        fields = {'ingredient',
                  'quantity',
                  'unit'
                  }
        labels = {
            'ingredient': 'Ingredient',
            'quantity': 'Quantity',
            'unit': 'Unit',
        }


class RecipeForm(forms.ModelForm):
    """Recipe Form"""

    category = forms.ModelChoiceField(
        queryset=RecipeCategory.objects.all(),
        widget=forms.Select()
    )

    class Meta:
        """
        Form Fields
        """
        model = Recipe
        fields = ("recipe",
                  "description",
                  "category",
                  "subcategory",
                  "portions",
                  )
        labels = {
            "recipe": "Recipe",
            "description": "Description",
            "category": "Category",
            "subcategory": "SubCategory",
            "portions": "Portions",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recipe'].widget.attrs['autofocus'] = True
        self.fields['description'].widget.attrs = {'rows': 3}


class MethodForm(forms.ModelForm):
    """Method form"""

    class Meta:
        """
        Form Fields
        """

        model = Method
        fields = ("steps",
                  )
        labels = {
            "steps": "Steps",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['steps'].widget.attrs = {'rows': 3}