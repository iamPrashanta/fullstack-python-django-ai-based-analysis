from django.core.management.base import BaseCommand
from apps.exhibitors.parser import parse_exhibitors


class Command(BaseCommand):
    help = 'Import exhibitors from txt file'

    def handle(self, *args, **kwargs):
        import os
        from django.conf import settings
        file_path = os.path.join(settings.BASE_DIR, 'apps', 'exhibitors', 'data', 'sample.txt')
        parse_exhibitors(file_path)
        self.stdout.write(self.style.SUCCESS('Import completed'))