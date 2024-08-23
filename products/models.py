from django.db import models
from django.contrib.auth.models import AbstractUser


class Category(models.Model):
    """ Creates Categories OF Products """
    class Meta:
        """ Gives the plural name of the model"""
        verbose_name_plural = 'Categories'

    category = models.CharField(max_length=30)

    def __str__(self):
        return str(self.category)


class Subcategory(models.Model):
    """ Creates Sub Categories of the Products """

    class Meta:
        """ Gives the plural name of the model"""
        verbose_name_plural = 'subcategories'

    category = models.ForeignKey(
        'Category', null=True, blank=True,
        on_delete=models.SET_NULL)
    subcategory = models.CharField(max_length=30)

    def __str__(self):
        return str(self.subcategory)


class Product(models.Model):
    """
    A model to create and manage Products
    """
    UNIT_CHOICE = (
        ('grams', 'g'),
        ('quantity', 'qty'),
        ('ml', 'ml'),
    )

    subcategory = models.ForeignKey(
        'Subcategory', null=True, blank=True,
        on_delete=models.SET_NULL
    )
    category = models.ForeignKey(
        'Category', null=True, blank=True,
        on_delete=models.SET_NULL
    )
    cost = models.DecimalField(
        max_digits=15,
        decimal_places=2,
    )
    product = models.CharField(
        max_length=254,
    )
    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        default=0
    )
    unit = models.CharField(
        max_length=10,
        choices=UNIT_CHOICE
    )

    class Meta:
        ordering = ["product"]

    def __str__(self):
        return f"{self.quantity}{self.unit} of {self.product} for {self.cost}"
