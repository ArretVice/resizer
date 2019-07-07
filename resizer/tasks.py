from celery import shared_task
from django.conf import settings


@shared_task
def resize_image_task(image_path, width, height):
    '''
    resize_image(<image>, <width>, <height>)
    Returns resized copy of <image_path>.
    '''
    return Image.open(image).resize((width, height))
