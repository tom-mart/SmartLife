from django.urls import path
from . import views

app_name = 'garage'

urlpatterns = [
    path('', views.index, name='index'),
]
