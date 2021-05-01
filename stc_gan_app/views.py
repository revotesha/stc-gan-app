from django.shortcuts import render
from django.http import HttpResponse
from .models import i2i_style_transfer
from django.core.files.storage import default_storage
import os
import sys

import numpy as np

from ...stc_gan_project.settings import LOGGING

import logging

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('MYAPP')
logger.info("Just testing")


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
        'meta_data':'Processing time: 20s &#10;&#13 Output image size: 24MB',
        'status':'Done!'
    }
]

# Create your views here.
def app_home(request):

    if request.method == 'POST':

        file = request.FILES['ImageFile']
        file_name = default_storage.save(file.name, file)
        file_url = default_storage.path(file_name)

    else:
        return render(request, 'stc_gan_app/upload_image.html', context)

    # access input_info and do something to it. output output_info

    context = {
        "input_info":input_info,
        "output_info":output_info
    }

    # remove image after we're done with it
    os.remove(file_url)

    return render(request, 'stc_gan_app/model_results.html', context)