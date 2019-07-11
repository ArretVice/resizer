from django.test import TestCase

from resizer.models import ProcessedTasks


class TestProcessedTasks(TestCase):

    def setUp(self):
        self.task_id = 'some task id'
        self.fake_task_id = 'fake task id'

    def test_task_creation(self):
        ProcessedTasks.objects.create(task_id=self.task_id)
        self.assertTrue(ProcessedTasks.objects.get(task_id=self.task_id))

    def test_fake_task(self):
        self.assertFalse(ProcessedTasks.objects.filter(task_id=self.fake_task_id))
