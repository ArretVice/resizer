import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from resizer.models import ProcessedTasks


class Command(BaseCommand):
    help = '''
         - Deletes all entries in the database about any resized images
         - Clears ./media/tmp folder
         - Deletes log file "resizer.log"
    '''

    def handle(self, *args, **options):
        # cleaning DB
        ProcessedTasks.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(' - Database cleaned'))

        # cleaning media/tmp folder
        path = os.path.join(settings.MEDIA_ROOT, 'tmp')
        for file in os.listdir(path):
            os.remove(os.path.join(path, file))
            self.stdout.write(self.style.SUCCESS(f' - Removed {file}'))
        self.stdout.write(self.style.SUCCESS(' - media/tmp folder cleaned'))

        # deleting log file
        os.remove(os.path.join(settings.BASE_DIR, 'resizer.log'))
        self.stdout.write(self.style.SUCCESS(' - Log file deleted'))
