from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.

class UploadedImage(models.Model):
    file = models.ImageField(upload_to='images/', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    channels = models.PositiveIntegerField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}: {self.file.name}"

class UploadedPDF(models.Model):
    file = models.FileField(upload_to='pdfs/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    pages = models.PositiveIntegerField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PDF {self.id}: {self.file.name}"
