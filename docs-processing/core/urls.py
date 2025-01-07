from django.urls import path
from .views import (
    RotateImageView,
    UploadFileView,
    ImageListView,
    PDFListView,
    ImageDetailView,
    PDFDetailView
)

urlpatterns = [
    path('upload/', UploadFileView.as_view(), name='file-upload'),
    path('images/', ImageListView.as_view(), name='image-list'),
    path('pdfs/', PDFListView.as_view(), name='pdf-list'),
    path('images/<int:pk>/', ImageDetailView.as_view(), name='image-detail-delete'),
    path('pdfs/<int:pk>/', PDFDetailView.as_view(), name='pdf-detail-delete'),
    path('rotate/', RotateImageView.as_view(), name='rotate-image'),
]
