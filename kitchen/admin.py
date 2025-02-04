from django.contrib import admin
from .models import Inventory, InventoryItem, InventoryItemPurchase, Recipe, RecipeIngredient

admin.site.register(Inventory)
admin.site.register(InventoryItem)
admin.site.register(InventoryItemPurchase)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
