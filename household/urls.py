from django.urls import path
from . import views

app_name = 'household'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_household, name='create'),
    path('join/', views.join_household, name='join'),
    path('leave/', views.leave_household, name='leave'),
]
