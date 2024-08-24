from django import forms
from .models import Product, Category, Subcategory


class ProductForm(forms.ModelForm):
    """ Product instance Form"""
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select()
    )
    subcategory = forms.ModelChoiceField(
        queryset=Subcategory.objects.all(),
        widget=forms.Select()
    )

    def clean_cost(self):
        """ Function To Raise Validation EError If Value Is 0"""
        cost = self.cleaned_data['cost']
        if cost <= 0:
            raise forms.ValidationError("Cost must be €0.01 or above")
        return cost
    
    def clean_quantity(self):
        """ Function To Raise Validation EError If Value Is 0"""
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be a 1 or above ")
        return quantity
    
    class Meta:
        """
        Form Fields
        """
        model = Product
        fields = ("product",
                  "category",
                  "subcategory",
                  "cost",
                  "unit",
                  "quantity",
                  )
        labels = {"product": "Product",
                  "category": "Category",
                  "subcategory": "Subcategory",
                  "cost": "Cost",
                  "unit": "Unit",
                  "quantity": "Quantity",
                  }