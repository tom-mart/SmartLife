from django.contrib import admin
from .models import Recipe, RecipeIngredient

admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
