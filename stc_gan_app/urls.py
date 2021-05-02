from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.app_home, name='stc-gan-app-home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
