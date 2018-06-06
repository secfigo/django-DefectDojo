import csv

from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from pytz import timezone

from dojo.models import Finding
from dojo.utils import get_system_setting

locale = timezone(get_system_setting('time_zone'))

"""
Author: Aaron Weaver
This script will extract all verified and active findings
"""


class Command(BaseCommand):
    help = 'Input: Filepath (under MEDIA_ROOT) and name'

    def add_arguments(self, parser):
        parser.add_argument('file_path')

    def handle(self, *args, **options):
        file_path = options['file_path']

        findings = Finding.objects.filter(verified=True,
                                          active=True).select_related(
            "test__engagement__product")
        fd = default_storage.open(file_path, 'w')
        writer = csv.writer(fd)

        headers = [
            "product_name",
            "id",
            "title",
            "cwe",
            "date",
            "url",
            "severity",
        ]

        writer.writerow(headers)
        for obj in findings:
            row = [obj.test.engagement.product]
            for field in headers:
                if field is not "product_name":
                    value = getattr(obj, field)
                    if isinstance(value, unicode):
                        value = value.encode('utf-8').strip()

                    row.append(value)
            writer.writerow(row)
