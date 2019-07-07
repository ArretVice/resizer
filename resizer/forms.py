from django import forms
from .models import UploadedImage


VALID_FORMATS = ['jpeg', 'jpg', 'png']
IMAGE_DIMENSIONS = {
    'height': {
        'min': 1,
        'max': 9999,
    },
    'width': {
        'min': 1,
        'max': 9999,
    },
}

class ImageUploadForm(forms.Form):
    image = forms.ImageField(required=True)
    width = forms.IntegerField(
        min_value=IMAGE_DIMENSIONS['width']['min'],
        max_value=IMAGE_DIMENSIONS['width']['max'],
        label=f"Width ({IMAGE_DIMENSIONS['width']['min']} - {IMAGE_DIMENSIONS['width']['max']} px)"
    )
    height = forms.IntegerField(
        min_value=IMAGE_DIMENSIONS['height']['min'],
        max_value=IMAGE_DIMENSIONS['height']['max'],
        label=f"Height ({IMAGE_DIMENSIONS['height']['min']} - {IMAGE_DIMENSIONS['height']['max']} px)"
    )

    # checking for valid image formats
    def clean_image(self):
        image = self.cleaned_data['image']
        image_format = image.name.split('.')[-1].lower()
        if image_format not in VALID_FORMATS:
            raise forms.ValidationError(f'Error: the image must be in one of the following formats: {", ".join(VALID_FORMATS)}.')
        return image
