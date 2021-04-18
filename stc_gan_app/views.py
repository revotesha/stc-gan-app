from django.shortcuts import render
from django.http import HttpResponse
from .models import i2i_style_transfer
import numpy as np

model_input = np.arange(100000).reshape(100, 1000)

model_output = i2i_style_transfer(model_input)

input_info = [
    {
        'type':'Input image',
        'data':model_input,
        'meta_data':'Input image size: 24MB',
        'status':'Processing ... Pleae wait. Output image will display on the right.'
    }
]

output_info = [
    {
        'type':'CycleGAN image',
        'data': model_output,
        'meta_data':'Processing time: 20s <br> Output image size: 24MB',
        'status':'Done!'
    }
]

# Create your views here.
def app_home(request):
    context = {
        "input_info":input_info,
        "output_info":output_info
    }
    return render(request, 'stc_gan_app/app_home.html', context)