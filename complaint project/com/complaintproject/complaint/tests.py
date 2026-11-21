from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase
import cv2
import numpy as np

from .forms import ComplaintForm, MAX_IMAGE_SIZE


class ComplaintFormTests(SimpleTestCase):
    def setUp(self):
        self.data = {
            'title': 'Broken lab light',
            'category': 'Lab',
            'description': 'The light is not working.',
        }

    def test_optional_photo_is_accepted_and_resized_with_opencv(self):
        image = np.zeros((1200, 2400, 3), dtype=np.uint8)
        success, encoded_image = cv2.imencode('.png', image)
        self.assertTrue(success)
        upload = SimpleUploadedFile(
            'lab-problem.png',
            encoded_image.tobytes(),
            content_type='image/png',
        )

        form = ComplaintForm(data=self.data, files={'image': upload})

        self.assertTrue(form.is_valid(), form.errors)
        processed_image = form.cleaned_data['image']
        self.assertEqual(processed_image.name, 'lab-problem.jpg')
        decoded_image = cv2.imdecode(
            np.frombuffer(processed_image.read(), dtype=np.uint8),
            cv2.IMREAD_COLOR,
        )
        self.assertEqual(decoded_image.shape[1], 1920)
        self.assertEqual(decoded_image.shape[0], 960)

    def test_photo_is_optional(self):
        form = ComplaintForm(data=self.data)

        self.assertTrue(form.is_valid(), form.errors)
        self.assertFalse(form.cleaned_data['image'])

    def test_invalid_photo_is_rejected(self):
        upload = SimpleUploadedFile(
            'not-an-image.jpg',
            b'not an image',
            content_type='image/jpeg',
        )

        form = ComplaintForm(data=self.data, files={'image': upload})

        self.assertFalse(form.is_valid())
        self.assertIn('image', form.errors)

    def test_oversized_upload_is_rejected_before_decoding(self):
        upload = SimpleUploadedFile(
            'large.jpg',
            b'x' * (MAX_IMAGE_SIZE + 1),
            content_type='image/jpeg',
        )

        form = ComplaintForm(data=self.data, files={'image': upload})

        self.assertFalse(form.is_valid())
        self.assertIn('5 MB or smaller', str(form.errors['image']))
