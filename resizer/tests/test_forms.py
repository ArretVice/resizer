import os
import random

from django.test import SimpleTestCase
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from resizer.forms import ImageUploadForm, CheckTaskByIDForm
from resizer.forms import VALID_FORMATS, MAX_FILE_SIZE, MAX_FILE_SIZE_MB, IMAGE_DIMENSIONS


test_path = os.path.join(settings.BASE_DIR, 'resizer/tests/test_images')
valid_images = {}
invalid_images = {}

for file in os.listdir(test_path):
    if file.split('.')[-1].lower() in VALID_FORMATS:
        if os.path.getsize(os.path.join(test_path, file)) <= MAX_FILE_SIZE:
            valid_images[file] = file
        else:
            invalid_images[file] = (file, 'invalid size')
    elif os.path.splitext(file)[-1] == '.txt':
        invalid_images[file] = (file, 'not an image')
    else:
        invalid_images[file] = (file, 'wrong format')


class TestImageUploadForm(SimpleTestCase):

    def test_valid_image_upload(self):
        for file in valid_images:
            upload_file = open(os.path.join(test_path, valid_images[file]), 'rb')
            post_dict = {'width': 500, 'height': 500}
            file_dict = {'image': SimpleUploadedFile(upload_file.name, upload_file.read())}
            form = ImageUploadForm(post_dict, file_dict)
            self.assertTrue(form.is_valid())

    def test_invalid_image_upload(self):
        for file in invalid_images:
            _, error = invalid_images[file]
            upload_file = open(os.path.join(test_path, invalid_images[file][0]), 'rb')
            post_dict = {'width': 500, 'height': 500}
            file_dict = {'image': SimpleUploadedFile(upload_file.name, upload_file.read())}
            form = ImageUploadForm(post_dict, file_dict)

            if error == 'invalid size':
                self.assertFalse(form.is_valid())
                self.assertEqual(
                    form.errors['image'][0],
                    f'Error: the image size exceeds {MAX_FILE_SIZE_MB} MB.'
                )
            elif error == 'wrong format':
                self.assertFalse(form.is_valid())
                self.assertEqual(
                    form.errors['image'][0],
                    f'Error: the image must be in one of the following formats: {", ".join(VALID_FORMATS)}.'
                )
            elif error == 'not an image':
                self.assertFalse(form.is_valid())
                self.assertEqual(
                    form.errors['image'][0],
                    'Upload a valid image. The file you uploaded was either not an image or a corrupted image.'
                )

    def test_valid_input_dimensions(self):
        valid_file = random.choice(list(valid_images))
        upload_file = open(os.path.join(test_path, valid_file), 'rb')
        file_dict = {'image': SimpleUploadedFile(upload_file.name, upload_file.read())}
        valid_dimensions = [
            (500, 500),
            (1, 1),
            (9999, 9999),
            (
                random.randint(
                    IMAGE_DIMENSIONS['width']['min'],
                    IMAGE_DIMENSIONS['width']['max']
                ),
                random.randint(
                    IMAGE_DIMENSIONS['height']['min'],
                    IMAGE_DIMENSIONS['height']['max']
                ),
            )
        ]

        if valid_file:
            for dims in valid_dimensions:
                post_dict = {'width': dims[0], 'height': dims[1]}
                form = ImageUploadForm(post_dict, file_dict)
                self.assertTrue(form.is_valid())

    def test_invalid_input_dimensions(self):
        valid_file = random.choice(list(valid_images))
        upload_file = open(os.path.join(test_path, valid_file), 'rb')
        file_dict = {'image': SimpleUploadedFile(upload_file.name, upload_file.read())}
        
        if valid_file:
            invalid_dims = [
                (100, -250),
                (0, 9999),
                (15, 10000),
            ]
            for dims in invalid_dims:
                post_dict = {'width': dims[0], 'height': dims[1]}
                form = ImageUploadForm(post_dict, file_dict)
                self.assertFalse(form.is_valid())


class TestCheckTaskByIDForm(SimpleTestCase):

    def test_string_input(self):
        form = CheckTaskByIDForm({'task_id': 'some_id123f 1234$ -#'})
        self.assertTrue(form.is_valid())

    def test_empty_input(self):
        form = CheckTaskByIDForm()
        self.assertFalse(form.is_valid())
