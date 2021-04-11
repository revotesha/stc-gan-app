from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='stc-gan-app-home'),
]
