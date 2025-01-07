import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import UploadedImage,UploadedPDF
@receiver(pre_delete, sender=UploadedImage)
def delete_image_file(sender, instance, **kwargs):
    # Delete the file from the media folder when the object is deleted
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

@receiver(pre_delete, sender=UploadedPDF)
def delete_pdf_file(sender, instance, **kwargs):
    # Delete the file from the media folder when the object is deleted
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)