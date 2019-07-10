import os

from PIL import Image
from django.test import SimpleTestCase, Client
from django.test import tag
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from resizer import views
from resizer import forms


class TestHomeView(SimpleTestCase):

    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get(reverse('resizer:home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'resizer/home.html')


class TestUploadAndResizeViewGet(SimpleTestCase):

    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get(reverse('resizer:upload'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'resizer/upload.html')
        self.assertIsInstance(response.context['form'], forms.ImageUploadForm)


# this test requires connection to message broker
@tag('slow')
class TestUploadAndResizeViewPost(SimpleTestCase):

    def setUp(self):
        self.client = Client()
        self.post_data = {'width': 500, 'height': 500}
        self.test_path = os.path.join(settings.BASE_DIR, 'resizer/tests/test_images')
        self.test_image = 'test_png_image.png'
        self.path = os.path.join(self.test_path, f'copied_{self.test_image}')
        self.copied_test_image = Image.open(os.path.join(self.test_path, self.test_image))
        self.copied_test_image.save(self.path)
        self.upload_file = open(self.path, 'rb')
        self.post_data['image'] = SimpleUploadedFile(self.upload_file.name, self.upload_file.read())
        self.post_data_invalid = self.post_data.copy()
        self.post_data_invalid['image'] = 'not an image'

    def tearDown(self):
        os.remove(self.path)

    def test_valid_post(self):
        response = self.client.post(reverse('resizer:upload'), self.post_data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'resizer/check_status.html')
        self.assertContains(response, response.context.get('task_id'))
        self.assertContains(response, response.context.get('task_status'))
        self.assertNotContains(response, response.context.get('form'))

    def test_invalid_post(self):
        response = self.client.post(reverse('resizer:upload'), self.post_data_invalid)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'resizer/upload.html')
        self.assertNotContains(response, response.context.get('task_id'))
        self.assertNotContains(response, response.context.get('task_status'))


class TestCheckStatusView(SimpleTestCase):

    def setUp(self):
        self.client = Client()
        self.post_data = {'task_id': 'some task ID 123980djweix 432-76@#$%'}
        self.redirect_url = reverse_lazy('resizer:task', kwargs={'task_id': self.post_data['task_id']})

    def test_get(self):
        response = self.client.get(reverse('resizer:check_status'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'resizer/check_status.html')
        self.assertIsInstance(response.context['form'], forms.CheckTaskByIDForm)

    def test_post(self):
        response = self.client.post(reverse('resizer:check_status'), self.post_data)
        self.assertEquals(response.status_code, 302)    # HTTP 302 - redirection
        self.assertRedirects(response, self.redirect_url)


class TestTaskStatusView(SimpleTestCase):

    def setUp(self):
        self.client = Client()
        self.task_id = 'some task ID 123980djweix 432-76@#$%'

    def test_get(self):
        response = self.client.get(reverse('resizer:task', args=[self.task_id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'resizer/check_status.html')
        self.assertContains(response, response.context.get('task_id'))
        self.assertContains(response, response.context.get('task_status'))
