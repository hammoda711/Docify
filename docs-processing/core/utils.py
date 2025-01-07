from rest_framework.response import Response
import os
import fitz  # PyMuPDF
from PIL import Image

def api_response(code, message, data=None, status_code=200):
    """
    Generate a standardized API response with an HTTP status code.
    :param code: 0 for success, 1 for errors
    :param message: Informative message about the response
    :param data: Any additional data (optional)
    :param status_code: HTTP status code (default is 200)
    :return: Standardized response with status code
    """
    return Response({"code": code, "message": message, "data": data}, status=status_code)


def convert_pdf_to_images(pdf_path, output_folder):
    # Create a folder for the converted images if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the PDF file using PyMuPDF
    pdf_document = fitz.open(pdf_path)

    # Loop through each page in the PDF and convert it to an image
    image_files = []
    for page_num in range(pdf_document.page_count):
        # Get the page from the PDF document
        page = pdf_document.load_page(page_num)

        # Render page to an image (pixmap)
        pixmap = page.get_pixmap()

        # Create a filename for the image (e.g., 'page_1.png')
        output_image_path = os.path.join(output_folder, f"page_{page_num + 1}.png")
        
        # Save the image
        pixmap.save(output_image_path)
        
        # Optionally, convert the image to other formats if needed (e.g., JPEG)
        image = Image.open(output_image_path)
        image_files.append(output_image_path)

    return image_files
