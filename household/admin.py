from django.contrib import admin
from .models import Household, CoOp, HouseholdMember
# Register your models here.

admin.site.register(Household)
admin.site.register(CoOp)
admin.site.register(HouseholdMember)