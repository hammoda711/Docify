from django.contrib import admin
from .models import UploadedImage, UploadedPDF

# Register your models here.
@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'width', 'height', 'channels', 'uploaded_at')

@admin.register(UploadedPDF)
class UploadedPDFAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'pages', 'uploaded_at')