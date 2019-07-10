from django.test import SimpleTestCase
from django.urls import reverse, resolve

from resizer import views


class TestUrls(SimpleTestCase):
    
    def test_home_url_is_resolved(self):
        url = reverse('resizer:home')
        self.assertEquals(resolve(url).func, views.home)

    def test_upload_url_is_resolved(self):
        url = reverse('resizer:upload')
        self.assertEquals(resolve(url).func.view_class, views.UploadAndResizeView)

    def test_check_status_url_is_resolved(self):
        url = reverse('resizer:check_status')
        self.assertEquals(resolve(url).func.view_class, views.CheckStatusView)

    def test_task_url_is_resolved(self):
        url = reverse('resizer:task', kwargs={'task_id': 'test_task_id'})
        self.assertEquals(resolve(url).func.view_class, views.TaskStatusView)
