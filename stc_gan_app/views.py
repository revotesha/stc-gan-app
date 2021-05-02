import os
import sys
import shutil

import numpy as np
from PIL import Image

from django.shortcuts import render
from django.http import HttpResponse
from .models import i2i_style_transfer
from django.core.files.storage import default_storage

# Create your views here.

def app_home(request):

    if request.method == 'POST':

        input_image = request.FILES['ImageFile']

        input_image_name = default_storage.save(input_image.name, input_image)
        input_image_size = (input_image.size)/(1024*1024)
        input_image_url = default_storage.path(input_image_name)

        ## validate file format and if not valid
        # if input_image not correct format:
        #   return render(request, 'stc_gan_app/upload_image.html')
        # add a line in upload_image.html to only show when file is invalid

        input_image_format = Image.open(input_image_url).format
        input_image_format = str(input_image_format).lower()
        if input_image_format not in ['JPEG', 'jpeg', 'PNG', 'png']:
            return render(request, 'stc_gan_app/upload_image.html')
            # doesn't work because it breaks before this step is reached

        input_image_name = 'input_image' + '.' + input_image_format
        shutil.copyfile(input_image_url, f'stc_gan_app/static/stc_gan_app/{input_image_name}')

        html_input_image_url = f'stc_gan_app/{input_image_name}'

        input_image_info = [
            {
                'type':'Input image',
                'data': html_input_image_url,
                'meta_data':f'Input image size: {round(input_image_size, 4)} Megabytes'
            }
        ]

    else:
        return render(request, 'stc_gan_app/upload_image.html')

    ## Image processing and modeling

    output_image = Image.open(f'stc_gan_app/static/stc_gan_app/{input_image_name}')

    # replace this with ML model
    output_image = output_image.convert(mode='L')
    output_image_format = input_image_format

    # save to file system
    output_image_name = 'output_image' + '.' + output_image_format

    output_image.save(f'stc_gan_app/static/stc_gan_app/{output_image_name}')

    output_image_size = (
        os.path.getsize(f'stc_gan_app/static/stc_gan_app/{output_image_name}')
    )
    output_image_size = output_image_size/(1024*1024)

    html_output_image_url = f'stc_gan_app/{output_image_name}' # shorter because
    # static works out the absolute path within model_results.html

    images = os.listdir('stc_gan_app/static/stc_gan_app/')

    output_image_info = [
        {
            'type':'CycleGAN image',
            'data': html_output_image_url,
            'meta_data':f'Processing time: 20s; Output image size: {round(output_image_size, 4)}'
        }
    ]

    context = {
        "input_info":input_image_info,
        "output_info":output_image_info
    }

    # remove image after we're done with it
    # os.remove(file_url) -- we need to somehow delete images when we're done

    return render(request, 'stc_gan_app/model_results.html', context)

sys.stdout.flush() # maybe you don't need this

# works but I think it'll break if user doesn't explicity add extension to file
# figure out how to dynamically pass file paths to model_results.html

# to run on heroku, remove path specification in Docker file
# ENV PORT = 8000
# and change $PORT to $PATH in the run_app.sh
# Reverse these to run locally