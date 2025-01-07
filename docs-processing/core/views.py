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