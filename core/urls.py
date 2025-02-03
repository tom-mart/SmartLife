from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)

urlpatterns = [
    path('', include('base.urls')),
    path('kitchen/', include('kitchen.urls')),
    path('garage/', include('garage.urls')),
    path('office/', include('office.urls')),
    path('household/', include('household.urls')),
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
