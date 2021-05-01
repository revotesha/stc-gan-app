import os
import sys

from django.shortcuts import render
from django.http import HttpResponse
from .models import i2i_style_transfer
from django.core.files.storage import default_storage

import numpy as np

# Create your views here.
def app_home(request):

    if request.method == 'POST':

        file = request.FILES['ImageFile']
        file_name = default_storage.save(file.name, file)
        file_size = (file.size)/(1024*1024)

        file_url = default_storage.path(file_name)

        input_info = [
            {
                'type':'Input image',
                'data': file_url, # we need to open this file and then close it after we're done
                'meta_data':f'Input image size: {file_size}'
            }
        ]

    else:
        return render(request, 'stc_gan_app/upload_image.html')

    # access input_info and do something to it. output output_info

    model_input = file.read()
    model_output = i2i_style_transfer(model_input)

    output_info = [
        {
            'type':'CycleGAN image',
            'data': model_output,
            'meta_data':'Processing time: 20s &#10;&#13 Output image size: 24MB'
        }
    ]

    context = {
        "input_info":input_info,
        "output_info":output_info
    }

    # remove image after we're done with it
    os.remove(file_url)

    return render(request, 'stc_gan_app/model_results.html', context)

sys.stdout.flush() # maybe you don't need this