from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .forms import ImageUploadForm
from .models import UploadedImage
from .functions import resize_image


IMAGE_DIMENSIONS = {
    'height': {
        'min': 1,
        'max': 9999,
    },
    'width': {
        'min': 1,
        'max': 9999,
    },
}
HEIGHT_RANGE = range(IMAGE_DIMENSIONS['height']['min'], IMAGE_DIMENSIONS['height']['max'] + 1)
WIDTH_RANGE = range(IMAGE_DIMENSIONS['width']['min'], IMAGE_DIMENSIONS['width']['max'] + 1)

# Create your views here.
def home(request):
    return render(request, 'resizer/home.html')

def upload(request):
    # add check for file format
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            return redirect('resizer:resize', image_id=image.pk)
    else:
        form = ImageUploadForm()
    return render(request, 'resizer/upload.html', {'form': form})

def resize(request, image_id):
    if request.method == 'POST':
        width = int(request.POST.get('width', None))
        height = int(request.POST.get('height', None))
        if (width in WIDTH_RANGE) and (height in HEIGHT_RANGE):
            image = UploadedImage.objects.get(pk=image_id).image
            # preserve image format by default
            image_extension = image.name.split('.')[-1].lower()
            if image_extension == 'jpg':
                image_extension = 'jpeg'
            resized_image = resize_image(image, width, height)
            response = HttpResponse(content_type=f"image/{image_extension}")
            resized_image.save(response, f'{image_extension.upper()}')
            return response
        else:
            messages.error(request, 'Error: image dimensions out of range.')
    image = UploadedImage.objects.get(pk=image_id)
    return render(request, 'resizer/resize.html', {'image': image})

def check_status(request, image_id):
    if request.method == 'POST':
        try:
            im_id = int(image_id)
        except:
            error = 'Image ID is incorrect.'
            return render(request, 'resizer/error_page.html', {'error': error})

        image = UploadedImage.objects.filter(id=im_id)[0]

        if image:
            return render(request, 'resizer/show_status.html', {'image': image.image})
        else:
            error = 'There is no image with this ID in the database.'
            return render(request, 'resizer/error_page.html', {'error': error})
    return redirect('resizer:status_page')

def status_page(request):
    return render(request, 'resizer/status_page.html')