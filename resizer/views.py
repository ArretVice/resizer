import os

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.core.files.storage import default_storage
from django.core.files.base import File
from django.conf import settings
from django.contrib import messages
from celery import current_app
from django.http import HttpResponseRedirect

from .forms import ImageUploadForm, CheckTaskByIDForm
from .tasks import resize_image_task
from .models import ProcessedTasks


# Create your views here.
class UploadAndResizeView(View):

    def get(self, request):
        form = ImageUploadForm()
        return render(request, 'resizer/upload.html', {'form': form})

    def post(self, request):
        form = ImageUploadForm(request.POST, request.FILES)
        context = {}
        if form.is_valid():
            image = File(request.FILES['image'])
            path = default_storage.save(f'tmp/{image.name}', image)
            path = os.path.join(settings.MEDIA_ROOT, path)
            task = resize_image_task.delay(
                image=path,
                width=int(request.POST['width']),
                height=int(request.POST['height']),
            )
            context['task_id'] = task.id
            context['task_status'] = task.status
            if task.status == 'PENDING':
                context['task_status'] = 'BEING PROCESSED'
            ProcessedTasks.objects.create(task_id=task.id)
            return render(request, 'resizer/check_status.html', context)
        context['form'] = form
        return render(request, 'resizer/upload.html', context)


class CheckStatusView(View):

    def get(self, request):
        form = CheckTaskByIDForm()
        return render(request, 'resizer/check_status.html', {'form': form})

    def post(self, request):
        form = CheckTaskByIDForm(request.POST)
        if form.is_valid():
            try:
                db_task_id = ProcessedTasks.objects.get(task_id=request.POST['task_id'])
                return HttpResponseRedirect(
                    reverse_lazy('resizer:task', kwargs={'task_id': request.POST['task_id']})
                )
            except:
                messages.error(request, f"Error: Image with ID: {request.POST['task_id']} does not exist.")
                return render(request, 'resizer/check_status.html', {'form': form})


class TaskStatusView(View):
    
    def get(self, request, task_id):
        task = current_app.AsyncResult(task_id)
        context = {
            'task_status': task.status,
            'task_id': task.id
        }
        if task.status == 'SUCCESS':
            context['resized_image_path'] = task.get()
        if task.status == 'PENDING':
            context['task_status'] = 'BEING PROCESSED'
        return render(request, 'resizer/check_status.html', context)


def home(request):
    return render(request, 'resizer/home.html')
