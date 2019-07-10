import os
import logging

from celery import shared_task
from PIL import Image
from django.conf import settings


media_root = settings.MEDIA_ROOT

# logger settings
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('resizer.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

@shared_task
def resize_image_task(image, width, height):
    '''
    resize_image(<image>, <width>, <height>)
    Returns path to resized copy of image.
    WARNING: initial image is deleted in the process, so consider passing copy of an image.
    '''
    initial_image = Image.open(image)
    filename = initial_image.filename.split('/')[-1]
    resized_image = initial_image.resize((width, height))
    relative_image_location = f'tmp/resized_{filename}'
    path = os.path.join(media_root, relative_image_location)
    resized_image.save(path)
    os.remove(image)
    logger.info(f'Resized {filename} to {width}x{height}')
    return relative_image_location
