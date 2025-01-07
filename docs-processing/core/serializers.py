from rest_framework import serializers
from .models import UploadedImage, UploadedPDF
from drf_extra_fields.fields import Base64ImageField, Base64FileField
from .validators import PDFBase64File, validate_file_name_length, validate_pdf_extension, validate_image_extension
from PyPDF2 import PdfReader
from io import BytesIO
from PIL import Image
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
    file = PDFBase64File(validators=[validate_file_name_length, validate_pdf_extension])
    pages = serializers.IntegerField(required=False)

    class Meta:
        model = UploadedPDF
        fields = ['id', 'file', 'pages', 'uploaded_at']

    def create(self, validated_data):
        # Save the file and extract the number of pages
        file = validated_data.get('file')
        pdf_file = file.read()

        # Extract the number of pages from the PDF
        pdf_reader = PdfReader(BytesIO(pdf_file))
        pages = len(pdf_reader.pages)

        # Create the UploadedPDF instance with extracted pages count
        uploaded_pdf = UploadedPDF.objects.create(
            file=file,
            pages=pages,
            uploaded_at=validated_data.get('uploaded_at')
        )
        return uploaded_pdf


