from django.shortcuts import render
from django.http import HttpResponse
from .models import i2i_style_transfer
import numpy as np

model_input = np.arange(100000).reshape(100, 1000)

model_output = i2i_style_transfer(model_input)

in_out_data = [

    {'type':'Input image',
     'data':model_input,
     'meta_data':'Input image size: 24MB',
     'status':'Processing ... Pleae wait. Output image will display on the right.'},

     {'type':'CycleGAN image',
     'data': model_output,
     'meta_data':'Processing time: 20s <br> Output image size: 24MB',
     'status':'Done!'}
]

# Create your views here.
def app_home(request):
    context = {
        "in_out_data":in_out_data
    }
    return render(request, 'stc_gan_app/app_home.html', context)