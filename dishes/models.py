from django.db import models
from django.db.models import Sum
from recipes.models import Recipe


class DishCategory(models.Model):
    """ Creates Categories for the Recipes """
    class Meta:
        """ Gives the plural name of the model"""
        verbose_name_plural = 'recipecategories'

    category = models.CharField(max_length=254)

    def __str__(self):
        return str(self.category)


class Dishes(models.Model):
    """
    A Model To Create Dessert Recipes
    """
    DISH_SUB_CAT=(
        ('hot', 'Hot'),
        ('cold', 'Cold'),
        ('other', 'Other'),
    )
    dish_name = models.CharField(
        max_length=300,
        null=False,
        blank=False
        )
    dish_description = models.CharField(
        max_length=500,
        null=False,
        blank=False
        )
    category = models.ForeignKey(
        'DishCategory', null=True, blank=True,
        on_delete=models.SET_NULL
    )
    subcategory = models.CharField(
        max_length=30,
        choices=DISH_SUB_CAT,
        null=True,
        blank=False
    )

    dish_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )

    RRP = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )

    def update_cost(self):
        """
        Updates cost when a new ingredient is added,
        """
        s_cost = self.dishsauce.aggregate(
            Sum(
                'sauce_cost'
            )
        )['sauce_cost__sum'] or 0
        e_cost = self.dishelement.aggregate(
            Sum(
                'element_cost'
            )
        )['element_cost__sum'] or 0
        sd_cost = self.dishsides.aggregate(
            Sum(
                'side_cost'
            )
        )['side_cost__sum'] or 0

        self.dish_cost = s_cost + e_cost + sd_cost
        
        self.RRP = self.dish_cost / 0.3
        self.save()

    class Meta:
        ordering = ["dish_name"]

    def __str__(self):
        return str(self.dish_name)


class DishSauce(models.Model):
    """
    A Model To Create Ingredients For The Recipes
    """
    dish = models.ForeignKey(
        Dishes,
        on_delete=models.CASCADE
        )
    dish_sauce = models.ForeignKey(
        Recipe,
        on_delete=models.
        SET_NULL,
        null=True,
        related_name="sauce"
        )
    sauce_cost = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        null=True,
        blank=False,
        editable=False
    )

    def save(self, *args, **kwargs):
        """
        Override the original save method to set and update the cost.
        """
        self.sauce_cost = self.dish_sauce.portion_cost
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.dish_sauce)


class DishElement(models.Model):
    """
    A Model To Add Elements To A Dessert Dish
    """
    dish = models.ForeignKey(
        Dishes,
        on_delete=models.CASCADE
        )
    dish_element = models.ForeignKey(
        Recipe,
        on_delete=models.
        SET_NULL,
        null=True,
        related_name="element"
        )
    element_cost = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        null=True,
        blank=False,
        editable=False
    )

    def save(self, *args, **kwargs):
        """
        Override the original save method to set and update the cost.
        """
        self.element_cost = self.dish_element.portion_cost
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.dish_element)


class DishSides(models.Model):
    """
    A Model To Add Elements To A Dessert Dish
    """
    dish = models.ForeignKey(
        Dishes,
        on_delete=models.CASCADE
        )
    dish_side = models.ForeignKey(
        Recipe,
        on_delete=models.
        SET_NULL,
        null=True,
        related_name="sides"
        )
    side_cost = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        null=True,
        blank=False,
        editable=False
    )

    def save(self, *args, **kwargs):
        """
        Override the original save method to set and update the cost.
        """
        self.side_cost = self.dish_side.portion_cost
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.dish_side)
