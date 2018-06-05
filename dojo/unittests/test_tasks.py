"""
Test Dojo tasks invoked via Celery
"""
from unittest import skip

from django.contrib.auth import get_user_model
from django.test import TestCase

from dojo.models import Report
from dojo.tasks import async_pdf_report


class PdfReportCreationTestCase(TestCase):
    @skip("Currently this test fails due to the dependency to wkhtmltopdf")
    def test_async_pdf_creation(self):
        # Prepare
        User = get_user_model()
        requestor = User.objects.create(username='FooUser', first_name='foo',
                                        last_name='bar')
        report = Report.objects.create(name="My Report", requester=requestor)
        context = {
            'host': 'myhost.local',
        }

        # Run
        result = async_pdf_report(report, context=context)

        # Verify
        self.assertTrue(result)
        report = Report.objects.get(id=report.id)
        self.assertNotEqual('error', report.status)
