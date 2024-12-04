from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import DishSauce, DishSides, DishElement

@receiver(post_save, sender=DishSauce)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update Cost on ingredientline update/create
    """
    instance.dishes.update_cost()

@receiver(post_delete, sender=DishSauce)
def update_on_delete(sender, instance, **kwargs):
    """
    Update Cost on ingredientline delete
    """
    instance.dishes.update_cost()

@receiver(post_save, sender=DishSides)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update Cost on ingredientline update/create
    """
    instance.dishes.update_cost()

@receiver(post_delete, sender=DishSides)
def update_on_delete(sender, instance, **kwargs):
    """
    Update Cost on ingredientline delete
    """
    instance.dishes.update_cost()

@receiver(post_save, sender=DishElement)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update Cost on ingredientline update/create
    """
    instance.dishes.update_cost()

@receiver(post_delete, sender=DishElement)
def update_on_delete(sender, instance, **kwargs):
    """
    Update Cost on ingredientline delete
    """
    instance.dishes.update_cost()

