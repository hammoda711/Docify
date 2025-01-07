from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from drf_extra_fields.fields import Base64FileField
import logging
logger = logging.getLogger(__name__)
import io
import PyPDF2
from rest_framework import serializers

def validate_file_name_length(file):
    if len(file.name) > 255:
        raise ValidationError(_('File name is too long.'))

def validate_pdf_extension(file):
    if not file.name.lower().endswith('.pdf'):
        raise ValidationError(_('Invalid file type. Only PDFs are allowed.'))

def validate_image_extension(file):
    valid_extensions = ['.jpg', '.jpeg', '.png']
    if not any(file.name.lower().endswith(ext) for ext in valid_extensions):
        raise ValidationError(_('Invalid file type. Allowed types: jpg, jpeg, png.'))

class PDFBase64File(Base64FileField):
    ALLOWED_TYPES = ['pdf']

    def get_file_extension(self, filename, decoded_file):
        # Validate the file is a proper PDF
        try:
            PyPDF2.PdfReader(io.BytesIO(decoded_file))  # Use PdfReader for modern PyPDF2
        except PyPDF2.errors.PdfReadError as e:
            logger.warning(f"Invalid PDF file: {e}")
            raise serializers.ValidationError("Uploaded file is not a valid PDF.")
        return 'pdf'