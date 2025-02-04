from django.db import models
from django.contrib.auth.models import User
from household.models import Household
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Inventory(models.Model):
    household = models.OneToOneField(Household, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.household.name})"

    class Meta:
        verbose_name_plural = "Pantries"

@receiver(post_save, sender=Household)
def create_household_pantry(sender, instance, created, **kwargs):
    """Create a Pantry automatically when a new Household is created"""
    if created:
        Inventory.objects.create(household=instance)

class InventoryItem(models.Model):

    class TypeChoices(models.TextChoices):
        PANTRY = 'pantry', 'Pantry'
        STOREROOM = 'storeroom', 'Storeroom'
        PRIVATE = 'private', 'Private'

    class UnitChoices(models.TextChoices):
        GRAMS = 'g', 'Grams'
        MILLILITERS = 'ml', 'Milliliters'
        PIECES = 'pcs', 'Pieces'

    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    inventory_type = models.CharField(max_length=20, choices=TypeChoices.choices)
    item_name = models.CharField(max_length=100, unique=True)
    generic_name = models.CharField(max_length=100, default='')
    quantity = models.FloatField()
    unit = models.CharField(max_length=10, choices=UnitChoices.choices)
 
    def __str__(self):
        return self.item_name

    def formatted_quantity(self):
        """Return quantity without decimal places if it's a whole number"""
        if self.quantity.is_integer():
            return str(int(self.quantity))
        return f"{self.quantity:.2f}"

    def display_amount(self):
        """Return formatted quantity with unit"""
        return f"{self.formatted_quantity()} {self.unit}"

    def get_purchase_stats(self):
        """Get purchase statistics for this item"""
        from django.db.models import Avg, Sum, Count
        from django.utils import timezone
        from datetime import timedelta

        # Get all purchases
        purchases = self.pantryitempurchase_set.all()
        
        # Get recent purchases (last 30 days)
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        recent_purchases = purchases.filter(date_purchased__gte=thirty_days_ago)

        stats = {
            'total_purchases': purchases.count(),
            'total_quantity': float(purchases.aggregate(Sum('quantity'))['quantity__sum'] or 0),
            'total_spent': float(purchases.aggregate(Sum('price'))['price__sum'] or 0),
            'average_price': float(purchases.aggregate(Avg('price'))['price__avg'] or 0),
            'recent_purchases': recent_purchases.count(),
            'recent_quantity': float(recent_purchases.aggregate(Sum('quantity'))['quantity__sum'] or 0),
            'recent_spent': float(recent_purchases.aggregate(Sum('price'))['price__sum'] or 0),
        }
        
        return stats

    class Meta:
        verbose_name_plural = "Pantry Items"

class InventoryItemAdditionalData(models.Model):
    item = models.OneToOneField(InventoryItem, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)

class InventoryItemPurchase(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=10, choices=InventoryItem.UnitChoices.choices)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    date_purchased = models.DateField()

class ItemPurchaseAdditionalData(models.Model):
    purchase = models.OneToOneField(InventoryItemPurchase, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)

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