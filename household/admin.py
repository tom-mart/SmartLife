from django.contrib import admin
from .models import Household, CoOp, HouseholdMember, Inventory, InventoryItem, InventoryItemPurchase
# Register your models here.

admin.site.register(Household)
admin.site.register(CoOp)
admin.site.register(HouseholdMember)
admin.site.register(Inventory)
admin.site.register(InventoryItem)
admin.site.register(InventoryItemPurchase)