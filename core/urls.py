from django.contrib import admin
from django.urls import path

from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
