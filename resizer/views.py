from django.shortcuts import render
from django.views import View
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .forms import ImageUploadForm
from .tasks import resize_image_task


# Create your views here.
class UploadAndResizeView(View):
    def get(self, request):
        form = ImageUploadForm()
        return render(request, 'resizer/upload.html', {'form': form})

    def post(self, request):
        form = ImageUploadForm(request.POST, request.FILES)
        context = {}
        if form.is_valid():
            file = request.FILES['image']
            filename, extension = file.name.split('.')
            path = default_storage.save(f'tmp/{filename}.{extension}', ContentFile(file.read()))
            task = resize_image_task.delay(
                image_path=path,
                width=request.POST['width'],
                height=request.POST['height'],
            )
            default_storage.delete(f'tmp/{filename}.{extension}')
            context['initial_image'] = file
            context['task_id'] = task.id
            context['task_status'] = task.status
            return render(request, 'resizer/upload.html', context)
        context['form'] = form
        return render(request, 'resizer/upload.html', context)


def home(request):
    return render(request, 'resizer/home.html')
