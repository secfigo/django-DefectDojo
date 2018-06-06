import os

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.test import TestCase

from dojo.finding.views import remove_finding_image_from_storage
from dojo.models import FindingImage


class FindingViewsTestCase(TestCase):
    def test_remove_finding_image_from_storage(self):
        """
        Test whether images are properly stored and removed
        """
        # Set up a FindingImage object, storing a file
        pseudo_image = ContentFile('image data, yay!', 'image.jpg')
        finding_image = FindingImage.objects.create(image=pseudo_image)
        file_under_media_root = os.path.join(FindingImage.UPLOAD_DIRECTORY,
                                             'image.jpg')
        self.assertTrue(default_storage.exists(file_under_media_root))

        # Run logic
        remove_finding_image_from_storage(finding_image)

        # Verify the file has disappeared
        self.assertFalse(default_storage.exists(file_under_media_root))
