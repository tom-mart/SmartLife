from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from household.models import HouseholdMember

@login_required
def index(request):
    try:
        household_member = request.user.household_member
        # User is part of a household, show regular dashboard
        return render(request, 'base/index.html')
    except HouseholdMember.DoesNotExist:
        # User is not part of a household, show household setup page
        return render(request, 'base/household_setup.html')