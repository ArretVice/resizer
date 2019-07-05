from django import forms
from .models import UploadedImage


VALID_FORMATS = ['jpeg', 'jpg', 'png']

class ImageUploadForm(forms.ModelForm):
    # checking for valid image formats
    def clean_image(self):
        image = self.cleaned_data['image']
        image_format = image.name.split('.')[-1].lower()
        if image_format not in VALID_FORMATS:
            raise forms.ValidationError(f'Error: the image must be in one of the following formats: {", ".join(VALID_FORMATS)}.')
        return image

    class Meta:
        model = UploadedImage
        fields = ('image', )
