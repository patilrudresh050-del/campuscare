from pathlib import Path

import cv2
import numpy as np
from django import forms
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError

from .models import Complaint


MAX_IMAGE_SIZE = 5 * 1024 * 1024
MAX_IMAGE_PIXELS = 40_000_000
MAX_IMAGE_DIMENSION = 1920


class ComplaintForm(forms.ModelForm):
    image = forms.FileField(
        required=False,
        label='Problem photo (optional)',
        help_text='Upload a JPG, PNG, or WebP image up to 5 MB.',
    )

    class Meta:
        model = Complaint
        fields = ('title', 'category', 'description', 'image')

    def clean_image(self):
        uploaded_image = self.cleaned_data.get('image')
        if not uploaded_image:
            return uploaded_image

        if uploaded_image.size > MAX_IMAGE_SIZE:
            raise ValidationError('The photo must be 5 MB or smaller.')

        image_bytes = np.frombuffer(uploaded_image.read(), dtype=np.uint8)
        image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
        if image is None:
            raise ValidationError('Upload a valid JPG, PNG, or WebP image.')

        height, width = image.shape[:2]
        if width * height > MAX_IMAGE_PIXELS:
            raise ValidationError('The photo dimensions are too large.')

        longest_side = max(width, height)
        if longest_side > MAX_IMAGE_DIMENSION:
            scale = MAX_IMAGE_DIMENSION / longest_side
            image = cv2.resize(
                image,
                (round(width * scale), round(height * scale)),
                interpolation=cv2.INTER_AREA,
            )

        success, processed_image = cv2.imencode(
            '.jpg',
            image,
            [cv2.IMWRITE_JPEG_QUALITY, 90],
        )
        if not success:
            raise ValidationError('The photo could not be processed.')

        filename = f'{Path(uploaded_image.name).stem}.jpg'
        return ContentFile(processed_image.tobytes(), name=filename)
