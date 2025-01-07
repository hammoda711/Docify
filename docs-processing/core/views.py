from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView
from .models import UploadedImage, UploadedPDF
from .serializers import UploadedImageSerializer, UploadedPDFSerializer
from .utils import api_response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView
from .models import UploadedImage, UploadedPDF
from .serializers import UploadedImageSerializer, UploadedPDFSerializer
from .utils import api_response

class UploadFileView(APIView):

    def post(self, request):
        if 'file_type' not in request.data or not request.data.get('file'):
            # Return 400 Bad Request for missing required fields
            return api_response(1, "file_type and file are required", status_code=400)

        file_type = request.data['file_type']
        if file_type == 'image':
            serializer = UploadedImageSerializer(data=request.data)
        elif file_type == 'pdf':
            serializer = UploadedPDFSerializer(data=request.data)
        else:
            # Return 400 Bad Request for invalid file_type
            return api_response(1, "Invalid file_type. Allowed values: 'image', 'pdf'", status_code=400)

        if serializer.is_valid():
            serializer.save()
            # Return 201 Created for successful file upload
            return api_response(0, "File uploaded successfully", serializer.data, status_code=201)
        
        # Return 422 Unprocessable Entity for validation errors
        return api_response(1, "Validation error", serializer.errors, status_code=422)


class ImageListView(ListAPIView):
    queryset = UploadedImage.objects.all()
    serializer_class = UploadedImageSerializer

class PDFListView(ListAPIView):
    queryset = UploadedPDF.objects.all()
    serializer_class = UploadedPDFSerializer


class ImageDetailView(RetrieveDestroyAPIView):
    queryset = UploadedImage.objects.all()
    serializer_class = UploadedImageSerializer

class PDFDetailView(RetrieveDestroyAPIView):
    queryset = UploadedPDF.objects.all()
    serializer_class = UploadedPDFSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from .models import UploadedImage
from .serializers import UploadedImageSerializer
from .utils import api_response

class RotateImageView(APIView):
    def post(self, request):
        image_id = request.data.get("image_id")
        angle = request.data.get("angle")

        if not image_id or not angle:
            return api_response(1, "Both 'image_id' and 'angle' are required.", status_code=400)

        try:
            angle = int(angle)
        except ValueError:
            return api_response(1, "'angle' must be an integer.", status_code=400)

        # Get the image instance
        image_instance = get_object_or_404(UploadedImage, id=image_id)
        image_path = image_instance.file.path

        try:
            # Open the image
            with Image.open(image_path) as img:
                rotated_img = img.rotate(-angle, expand=True)  # Rotate counter-clockwise by default
                
                # Save the rotated image to the same file
                rotated_img.save(image_path, format=img.format)

            # Return a success response
            return api_response(
                0,
                "Image rotated successfully.",
                UploadedImageSerializer(image_instance).data,
                status_code=200
            )
        except Exception as e:
            return api_response(1, f"Error rotating image: {str(e)}", status_code=500)
