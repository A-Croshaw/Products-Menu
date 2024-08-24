from django.db import models
from django.db.models import Sum
from products.models import Product


class RecipeCategory(models.Model):
    """ Creates Categories for the Recipes """
    class Meta:
        """ Gives the plural name of the model"""
        verbose_name_plural = 'recipecategories'

    category = models.CharField(max_length=254)

    def __str__(self):
        return str(self.category)


class Recipe(models.Model):
    """A Model To Create A Recipes"""
    RECIPE_SUB_CAT=(
        ('hot', 'Hot'),
        ('cold', 'Cold'),
        ('other', 'Other'),
    )

    recipe = models.CharField(
        max_length=200,
        null=True,
        blank=False
    )
    description = models.TextField()
    category = models.ForeignKey(
        'RecipeCategory', null=True, blank=True,
        on_delete=models.SET_NULL
    )
    subcategory = models.CharField(
        max_length=30,
        choices=RECIPE_SUB_CAT,
        null=True,
        blank=False
    )
    cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    portions = models.DecimalField(
        max_digits=10, decimal_places=0, default=0
    )
    portion_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )

    def update_cost(self):
        """
        Updates cost when a new ingredient is added,
        """
        self.cost = self.ingredients.aggregate(
            Sum(
                'ingredient_cost'
            )
        )['ingredient_cost__sum'] or 0

        self.portion_cost = self.cost / self.portions
        self.save()

    class Meta:
        ordering = ["recipe"]

    def __str__(self):
        return str(self.recipe)


class Ingredients(models.Model):
    """A Model To Create Ingredients For The Recipes"""
    UNITS = (
    ('g', 'g'),
    ('ml', 'ml'),
    ('qty', 'qty'),
    )
    recipe = models.ForeignKey(
        Recipe,
        null=False, blank=False,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    ingredient = models.ForeignKey(
        Product,
        on_delete=models.
        SET_NULL,
        null=True,
        related_name="ingredients"
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=0
    )
    unit = models.CharField(
        max_length=5,
        choices=UNITS,
        default="g",
    )
    ingredient_cost = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=False,
        editable=False
    )
    
    def save(self, *args, **kwargs):
        """
        Override the original save method to set the ingredientline_total
        and update the cost.
        """
        self.ingredient_cost =  (
                self.ingredient.cost / self.ingredient.quantity) * self.quantity
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["recipe"]

    def __str__(self):
        return str(self.ingredient)


class Method(models.Model):
    """A Model To Create Steps For The Recipe"""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    steps = models.TextField(null=True)

    def __str__(self):
        return str(self.steps)
