from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def app_home(request):
    return render(request, 'stc_gan_app/app_home.html')