from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import uuid

from .models import Household, HouseholdMember

# Create your views here.

@login_required
def index(request):
    try:
        household_member = request.user.household_member
        household = household_member.household
        members = household.members.select_related('user').all()
        
        context = {
            'household': household,
            'members': members,
            'join_code': household.join_code,
            'user_joined_at': household_member.joined_at,
        }
        return render(request, 'household/index.html', context)
    except HouseholdMember.DoesNotExist:
        messages.error(request, 'You are not part of any household')
        return redirect('base:index')

@login_required
def create_household(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            # Generate a unique join code
            join_code = str(uuid.uuid4())[:8].upper()
            
            # Create the household
            household = Household.objects.create(
                name=name,
                join_code=join_code
            )
            
            # Add the current user as a member
            HouseholdMember.objects.create(
                user=request.user,
                household=household
            )
            
            messages.success(request, f'Successfully created household: {name}')
            return redirect('base:index')
        else:
            messages.error(request, 'Please provide a household name')
    
    return redirect('base:index')

@login_required
def join_household(request):
    if request.method == 'POST':
        join_code = request.POST.get('join_code')
        if join_code:
            try:
                household = Household.objects.get(join_code=join_code)
                
                # Check if user is already in a household
                if hasattr(request.user, 'household_member'):
                    messages.error(request, 'You are already a member of a household')
                    return redirect('base:index')
                
                # Add the user to the household
                HouseholdMember.objects.create(
                    user=request.user,
                    household=household
                )
                
                messages.success(request, f'Successfully joined household: {household.name}')
                return redirect('base:index')
            
            except Household.DoesNotExist:
                messages.error(request, 'Invalid join code')
        else:
            messages.error(request, 'Please provide a join code')
    
    return redirect('base:index')

@login_required
def leave_household(request):
    if request.method == 'POST':
        try:
            household_member = request.user.household_member
            household_name = household_member.household.name
            
            # Delete the household member
            household_member.delete()
            
            messages.success(request, f'Successfully left household: {household_name}')
        except HouseholdMember.DoesNotExist:
            messages.error(request, 'You are not part of any household')
    
    return redirect('base:index')
