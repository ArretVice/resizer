from django.shortcuts import render, redirect, get_object_or_404
from .forms import ImageUploadForm
from .models import UploadedImage


# Create your views here.
def home(request):
    return render(request, 'resizer/home.html')

def upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            return redirect('resizer:resize', image_id=image.pk)
    else:
        form = ImageUploadForm()
    return render(request, 'resizer/upload.html', {'form': form})

def resize(request, image_id):
    ### continue from here
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)#
        if form.is_valid():#
            image = form.save()#
            return redirect('resizer:resize', image_id=image.pk)#
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