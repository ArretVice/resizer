import os

from PIL import Image
from django.conf import settings
from django.test import SimpleTestCase

from resizer.tasks import resize_image_task




class TestResizeImageTask(SimpleTestCase):

    def setUp(self):
        self.test_path = os.path.join(settings.BASE_DIR, 'resizer/tests/test_images')
        self.test_image = 'test_png_image.png'
        self.path = os.path.join(self.test_path, f'copied_{self.test_image}')
        self.copied_test_image = Image.open(os.path.join(self.test_path, self.test_image))
        self.copied_test_image.save(self.path)
        self.log_file = os.path.join(settings.BASE_DIR, 'resizer.log')
        self.width, self.height = (500, 500)

    def test_resize_image_task(self):
        resized_image = resize_image_task(
            image=self.path,
            width=self.width,
            height=self.height
        )

        # test return value
        self.assertIsInstance(resized_image, str)

        # test image dimensions
        resized_image_opened = Image.open(os.path.join(settings.MEDIA_ROOT, resized_image))
        result_width, result_height = resized_image_opened.size
        self.assertEquals((result_width, result_height), (self.width, self.height))

        # test if operation was logged properly
        proper_log_entry = f"Resized {self.path.split('/')[-1]} to {self.width}x{self.height}\n"
        with open(self.log_file, 'r') as f:
            for line in f.readlines():
                pass # reading entire file is not efficient
            last_line = line
        self.assertTrue(last_line.endswith(proper_log_entry))
