# **Document Processing API Documentation**

## **Overview**

This API provides a suite of document processing services, allowing users to upload image and PDF files, perform various operations such as rotating images and converting PDFs to images, and retrieve detailed information about the files. The service is built using Django and Django Rest Framework (DRF), with Dockerization for seamless deployment. The API supports various file manipulation tasks with full integration of error handling, validation, and robust file management.

## **Table of Contents**

1. **Project Overview**
2. **Technologies Used**
3. **API Endpoints**
4. **Error Handling and Validation**
5. **Docker Setup**
6. **Postman collection**

---

## **1. Project Overview**

The Document Processing API allows users to upload images and PDF files, which are then processed and stored on the server. The API exposes multiple endpoints that enable operations such as rotating images, converting PDFs to images, and retrieving detailed metadata about uploaded files. The core objectives of the API include:

- File uploads in base64 format.
- Image rotation and PDF to image conversion.
- Detailed metadata retrieval for both images and PDFs.
- Seamless integration with Docker.

The service is designed to be flexible, scalable, and easy to integrate with other services. It supports error handling, validation, and ensures a smooth user experience.

---

## **2. Technologies Used**

- **Django**: A Python-based web framework used for building the API.
- **Django Rest Framework (DRF)**: A toolkit for building Web APIs in Django, making it easier to create RESTful endpoints.
- **PostgreSQL**: The database used to store file paths and metadata of the uploaded files.
- **Docker**: Containerization platform used for deployment and testing, ensuring a consistent environment.

## **3. API Endpoints**

### **File Upload and Metadata Retrieval**

#### **POST /api/upload/**

- **Description**: Accepts image and PDF files in base64 format and saves them to the server.
  
- **Request Body**:
  
  - `file`: Base64 encoded image or PDF file.
  
  Example:
  
  ```json
  {
      "file_type": "image",
      "file": "base64_string_here"
  }
  ```
  
- **Responses**:
  
  - `201 Created`: File uploaded successfully.
  - `400 Bad Request`: Missing required fields or invalid `file_type`.
  - `422 Unprocessable Entity`: Validation errors in the file upload.

---

#### **GET /api/images/**

- **Description**: Returns a list of all uploaded images.
  
- **Response**:
  
  - `200 OK`: List of uploaded images.
  
  Example:
  
  ```json
  [
    {
      "id": 1,
      "file": "image1.jpg",
      "width": 1920,
      "height": 1080,
      "channels": 3,
      "uploaded_at": "2025-01-07T22:05:56.449568Z"
    },
    {
      "id": 2,
      "file": "image2.jpg",
      "width": 1600,
      "height": 900,
      "channels": 3,
      "uploaded_at": "2025-01-07T22:05:56.449568Z"
    }
  ]
  ```
  

---

#### **GET /api/pdfs/**

- **Description**: Returns a list of all uploaded PDFs.
  
- **Response**:
  
  - `200 OK`: List of uploaded PDFs.
  
  Example:
  
  ```json
  [
    {
      "id": 1,
      "file": "document1.pdf",
      "uploaded_at": "2025-01-10T12:00:00Z",
      "number_of_pages": 5,
      "page_width": 595,
      "page_height": 842
    }
  ]
  ```
  

---

#### **GET /api/images/{id}/**

- **Description**: Returns detailed information about a specific image.
  
- **Parameters**: `id` (integer) - The ID of the image.
  
- **Response**:
  
  - `200 OK`: Image details.
  
  Example:
  
  ```json
  {
    "id": 1,
    "file": "image1.jpg",
    "uploaded_at": "2025-01-10T12:00:00Z",
    "width": 1920,
    "height": 1080,
    "channels": 3
  }
  ```
  

---

#### **GET /api/pdfs/{id}/**

- **Description**: Returns detailed information about a specific PDF.
  
- **Parameters**: `id` (integer) - The ID of the PDF.
  
- **Response**:
  
  - `200 OK`: PDF details.
  
  Example:
  
  ```json
  {
    "id": 1,
    "file": "document1.pdf",
    "uploaded_at": "2025-01-10T12:00:00Z",
    "number_of_pages": 5,
    "page_width": 595,
    "page_height": 842
  }
  ```
  

---

#### **DELETE /api/images/{id}/**

- **Description**: Deletes a specific image.
- **Parameters**: `id` (integer) - The ID of the image to be deleted.
- **Response**:
  - `204 No Content`: Image successfully deleted.
  - `404 Not Found`: Image not found.

---

#### **DELETE /api/pdfs/{id}/**

- **Description**: Deletes a specific PDF.
- **Parameters**: `id` (integer) - The ID of the PDF to be deleted.
- **Response**:
  - `204 No Content`: PDF successfully deleted.
  - `404 Not Found`: PDF not found.

---

#### **POST /api/rotate/**

- **Description**: Accepts an image ID and a rotation angle, rotates the image, and returns the rotated image.
  
- **Request Body**:
  
  - `id`: The ID of the image to be rotated.
  - `angle`: The angle by which to rotate the image (in degrees).
  
  Example:
  
  ```json
  {
    "image_id": 1,
    "angle": 90
  }
  ```
  
- **Responses**:
  
  - `200 OK`: Image rotated successfully.
  - `400 Bad Request`: Missing or invalid fields.
  - `404 Not Found`: Image with the specified ID not found.
  - `500 Internal Server Error`: Errors during image rotation.

---

#### **POST /api/convert-pdf-to-image/**

- **Description**: Accepts a PDF ID, converts the PDF to an image, and returns the image.
  
- **Request Body**:
  
  - `id`: The ID of the PDF to be converted.
  
  Example:
  
  ```json
  {
    "pdf_id": 1
  }
  ```
  
- **Responses**:
  
  - `200 OK`: PDF converted successfully, with the list of image files.
  - `400 Bad Request`: Missing `pdf_id`.
  - `404 Not Found`: PDF with the specified ID not found.

---

## **4. Error Handling and Validation**

This section describes the validation rules and file-handling processes implemented in the application.

#### **Validation Functions**

The following functions ensure the integrity and validity of uploaded files:

1. **`validate_file_name_length(file)`**
  
  - Validates the length of the uploaded file's name.
  - **Condition**: The file name must not exceed 255 characters.
  - **Error Raised**: `ValidationError` with the message: `"File name is too long."`
2. **`validate_pdf_extension(file)`**
  
  - Ensures the uploaded file has a `.pdf` extension.
  - **Condition**: The file name must end with `.pdf`.
  - **Error Raised**: `ValidationError` with the message: `"Invalid file type. Only PDFs are allowed."`
3. **`validate_image_extension(file)`**
  
  - Validates that the uploaded file is an image with one of the allowed extensions (`.jpg`, `.jpeg`, `.png`).
  - **Condition**: The file name must end with one of the allowed extensions.
  - **Error Raised**: `ValidationError` with the message: `"Invalid file type. Allowed types: jpg, jpeg, png."`

#### **Custom Fields**

- **`PDFBase64File`**
  - A custom file field for handling Base64-encoded PDF uploads.
  - **Allowed File Type**: PDF
  - **Validation**:
    - Uses `PyPDF2.PdfReader` to ensure the uploaded file is a valid PDF.
    - **Error Raised**: `serializers.ValidationError` with the message: `"Uploaded file is not a valid PDF."`

---

## **5. Docker Setup**

you will need to use both `Dockerfile`and `docker-compose.yml`.

### **Steps to Run the Application Using Docker**

1. **Install Docker and Docker Compose**
  
  - Ensure Docker and Docker Compose are installed on your system.
2. **Build and Run the Containers**
  
  - Use the following command to build and run the containers:
    
    `docker-compose up --build`
    
3. **Access the Application**
  
  - The application will be available at `http://localhost:8000`.
4. **Database Configuration**
  
  - The PostgreSQL database is set up as a service in the `docker-compose.yml` file. Use the following environment variables to connect:
    - `POSTGRES_USER`: `your_db_user`
    - `POSTGRES_PASSWORD`: `your_db_password`
    - `POSTGRES_DB`: `your_db_name`
5. **Stopping Containers**
  
  - To stop the running containers, use:
    
    `docker-compose down`
    

---

## **6. Deployment**

To deploy the project, ensure that the application is Dockerized, and follow these steps:

1. Build the Docker container using `docker-compose build`.
2. Run the application using `docker-compose up`.
3. Deploy on a platform like **PythonAnywhere** or any other hosting solution.

---

## **7. Postman collection**

For more detailed information on how to interact with the API, please refer to the **Postman collection**, you will find a full appraoch to interact with the project.

## Note:
You will need to create your own `.env` file, here is an exaple of `.env` :

```.md
# .env.example

# Django settings
SECRET_KEY="your-django-secret-key"
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database configuration
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_postgres_db_host
DB_PORT=5432

```
