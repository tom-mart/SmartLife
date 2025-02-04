from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from base.decorators import household_required

# Create your views here.

@login_required
@household_required
def index(request):
    return render(request, 'garage/index.html')
