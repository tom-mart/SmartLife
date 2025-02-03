from django.db import models
from django.contrib.auth.models import User


class Household(models.Model):
    name = models.CharField(max_length=100)
    join_code = models.CharField(max_length=8, unique=True)
    coop = models.ForeignKey('CoOp', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_default_household(cls):
        household, _ = cls.objects.get_or_create(
            name="Default Household",
            defaults={'join_code': 'DEFAULT1'}
        )
        return household.name

class HouseholdMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='household_member')
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name='members')
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.household.name}"
    
class CoOp(models.Model):
    name = models.CharField(max_length=100)
    join_code = models.CharField(max_length=8, unique=True)
    def __str__(self):
        return self.name
    
    @classmethod
    def get_default_coop(cls):
        coop, _ = cls.objects.get_or_create(
            name="Default CoOp",
            defaults={'join_code': 'DEFAULT1'}
        )
        return coop.name