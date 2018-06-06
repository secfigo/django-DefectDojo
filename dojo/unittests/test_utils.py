from datetime import datetime, timedelta

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.test import TestCase

from dojo.models import Engagement, Product
from dojo.utils import handle_uploaded_threat


class UtilsTestCase(TestCase):
    def test_threat_model_upload_handling(self):
        file = ContentFile("my content", 'file.txt')
        product = Product.objects.create(name="My product")
        engagement = Engagement.objects.create(name="My fabolous engagement",
                                               target_start=datetime.now() -
                                                            timedelta(days=1),
                                               target_end=datetime.now(),
                                               product=product)
        handle_uploaded_threat(file, engagement)

        updated_engagement = Engagement.objects.get(id=engagement.id)
        self.assertTrue(default_storage.exists(updated_engagement.tmodel_path))
