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
    def clean_portions(self):
        """ Function To Raise Validation Error If Value Is 0"""
        portions = self.cleaned_data['portions']
        if portions <= 0:
            raise forms.ValidationError("Portions must be a 1 or above ")
        return portions
    class Meta:
        """
        Form Fields
        """
        model = Recipe
        fields = ("recipe_name",
                  "description",
                  "category",
                  "subcategory",
                  "portions",
                  )
        labels = {
            "recipe_name": "Recipe",
            "description": "Description",
            "category": "Category",
            "subcategory": "Subcategory",
            "portions": "Portions",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recipe_name'].widget.attrs['autofocus'] = True
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