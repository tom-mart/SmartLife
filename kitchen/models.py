from django.db import models
from django.contrib.auth.models import User
from household.models import InventoryItem
from django.utils import timezone

class Recipe(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    recipe_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    prep_time = models.DurationField(blank=True, null=True)
    cook_time = models.DurationField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.recipe_name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    pantry_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.pantry_item.item_name} - {self.quantity} {self.unit}"