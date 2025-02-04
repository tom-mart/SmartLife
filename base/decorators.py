from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from household.models import HouseholdMember

def household_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            request.user.household_member
            return view_func(request, *args, **kwargs)
        except HouseholdMember.DoesNotExist:
            messages.warning(request, 'You need to join or create a household first.')
            return redirect('household:index')
    return _wrapped_view
