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

        ## get files
        first_image = request.FILES['FirstImageFile']
        second_image = request.FILES['SecondImageFile']

        ## get transfer direction
        direction = request.POST.get('style_direction')

        from_image = first_image
        to_image = second_image

        if direction == "two_to_one":
            from_image = second_image
            to_image = first_image

        ## image file attributes
        from_image_name = default_storage.save(from_image.name, from_image)
        to_image_name = default_storage.save(to_image.name, to_image)

        from_image_size = (from_image.size)/(1024*1024)
        to_image_size = (to_image.size)/(1024*1024)

        from_image_url = default_storage.path(from_image_name)
        to_image_url = default_storage.path(to_image_name)

        from_image_format = Image.open(from_image_url).format
        to_image_format = Image.open(to_image_url).format

        from_image_format = str(from_image_format).lower()
        to_image_format = str(to_image_format).lower()

        # if from_image_format not in ['JPEG', 'jpeg', 'PNG', 'png']:
        #     return render(request, 'stc_gan_app/upload_image.html')
        #     # doesn't work because it breaks before this step is reached

        ## move image files to static folder for easy accessibility
        from_image_name = 'from_image' + '.' + from_image_format
        to_image_name = 'to_image' + '.' + to_image_format

        shutil.copyfile(from_image_url, f'stc_gan_app/static/stc_gan_app/{from_image_name}')
        shutil.copyfile(to_image_url, f'stc_gan_app/static/stc_gan_app/{to_image_name}')

        ## maybe try use this to access images from html template
        html_from_image_url = f'stc_gan_app/{from_image_name}'
        html_to_image_url = f'stc_gan_app/{to_image_name}'

        ## output information for to_image
        to_image_info = [
            {
                'type':'Original image',
                'data': html_to_image_url,
                'meta_data':f'Original image size: {round(to_image_size, 2)}MB'
            }
        ]

    else:
        return render(request, 'stc_gan_app/upload_image.html')

    ## image processing and modeling

    output_image = Image.open(f'stc_gan_app/static/stc_gan_app/{to_image_name}')

    ## modeling: replace this with ML model
    output_image = output_image.convert(mode='L')
    output_image_format = from_image_format

    ## save model output  file to static folder
    output_image_name = 'output_image' + '.' + output_image_format
    output_image.save(f'stc_gan_app/static/stc_gan_app/{output_image_name}')

    ## output information for cyclegan image
    output_image_size = (
        os.path.getsize(f'stc_gan_app/static/stc_gan_app/{output_image_name}')
    )
    output_image_size = output_image_size/(1024*1024)

    html_output_image_url = f'stc_gan_app/{output_image_name}' # shorter because
    # static works out the absolute path within model_results.html

    output_image_info = [
        {
            'type':'CycleGAN image',
            'data': html_output_image_url,
            'meta_data':f'Processing time: 20s; Output image size: {round(output_image_size, 2)}MB'
        }
    ]

    context = {
        "input_info":to_image_info,
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

# add download button for the processed image