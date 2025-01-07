from rest_framework import serializers
from .models import UploadedImage, UploadedPDF
from drf_extra_fields.fields import Base64ImageField, Base64FileField
from .validators import PDFBase64File, validate_file_name_length, validate_pdf_extension, validate_image_extension
import logging
from PIL import Image
logger = logging.getLogger(__name__)

class UploadedImageSerializer(serializers.ModelSerializer):
    file = Base64ImageField(validators=[validate_file_name_length, validate_image_extension])

    class Meta:
        model = UploadedImage
        fields = ['id', 'file', 'width', 'height', 'channels', 'uploaded_at']

    def create(self, validated_data):
        # Save the image file
        instance = super().create(validated_data)

        # Open the image to extract dimensions and channels
        file = validated_data.get('file')
        image = Image.open(file)

        # Update the instance with width, height, and channels
        instance.width, instance.height = image.size
        instance.channels = len(image.getbands())  # e.g., RGB: 3, RGBA: 4
        instance.save()

        return instance


class UploadedPDFSerializer(serializers.ModelSerializer):
    file = PDFBase64File()

    class Meta:
        model = UploadedPDF
        fields = ['id', 'file', 'pages', 'uploaded_at']


