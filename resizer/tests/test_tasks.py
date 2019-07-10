import os

from PIL import Image
from django.conf import settings
from django.test import SimpleTestCase

from resizer.tasks import resize_image_task


test_path = os.path.join(settings.BASE_DIR, 'resizer/tests/test_images')
test_image = 'test_png_image.png'
path = os.path.join(test_path, f'copied_{test_image}')
copied_test_image = Image.open(os.path.join(test_path, test_image))
copied_test_image.save(path)
log_file = os.path.join(settings.BASE_DIR, 'resizer.log')

width, height = (500, 500)

class TestResizeImageTask(SimpleTestCase):

    def test_resize_image_task(self):
        resized_image = resize_image_task(
            image=path,
            width=width,
            height=height
        )

        # test return value
        self.assertIsInstance(resized_image, str)

        # test image dimensions
        resized_image_opened = Image.open(os.path.join(settings.MEDIA_ROOT, resized_image))
        result_width, result_height = resized_image_opened.size
        self.assertEquals((result_width, result_height), (width, height))

        # test if operation was logged properly
        proper_log_entry = f"Resized {path.split('/')[-1]} to {width}x{height}\n"
        with open(log_file, 'r') as f:
            for line in f.readlines():
                pass # reading entire file is not efficient
            last_line = line
        self.assertTrue(last_line.endswith(proper_log_entry))
