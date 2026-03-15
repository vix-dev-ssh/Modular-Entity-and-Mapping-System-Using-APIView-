# Django Intern Assignment - CertAI

This project implements a modular Django REST Framework backend using APIView only.

## Tech Stack
- Django
- Django REST Framework
- drf-yasg
- SQLite

## Project Structure

### Master Apps
- vendor
- product
- course
- certification

### Mapping Apps
- vendor_product_mapping
- product_course_mapping
- course_certification_mapping

Each app contains:
- models.py
- serializers.py
- views.py
- urls.py
- admin.py

## Requirements
Install dependencies:

```bash
python -m pip install django djangorestframework drf-yasg
```

## Setup Steps
1. Clone the repository
2. Move to project directory
3. Install dependencies
4. Run migrations
5. Start server

Example commands:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

## Installed Apps (Custom)
- vendor
- product
- course
- certification
- vendor_product_mapping
- product_course_mapping
- course_certification_mapping

## API Documentation
- Swagger UI: /swagger/
- ReDoc: /redoc/

## API Base Path
All APIs are under `/api/`.

## Master APIs
### Vendor
- GET /api/vendors/
- POST /api/vendors/
- GET /api/vendors/{id}/
- PUT /api/vendors/{id}/
- PATCH /api/vendors/{id}/
- DELETE /api/vendors/{id}/

### Product
- GET /api/products/
- POST /api/products/
- GET /api/products/{id}/
- PUT /api/products/{id}/
- PATCH /api/products/{id}/
- DELETE /api/products/{id}/

### Course
- GET /api/courses/
- POST /api/courses/
- GET /api/courses/{id}/
- PUT /api/courses/{id}/
- PATCH /api/courses/{id}/
- DELETE /api/courses/{id}/

### Certification
- GET /api/certifications/
- POST /api/certifications/
- GET /api/certifications/{id}/
- PUT /api/certifications/{id}/
- PATCH /api/certifications/{id}/
- DELETE /api/certifications/{id}/

## Mapping APIs
### Vendor Product Mapping
- GET /api/vendor-product-mappings/
- POST /api/vendor-product-mappings/
- GET /api/vendor-product-mappings/{id}/
- PUT /api/vendor-product-mappings/{id}/
- PATCH /api/vendor-product-mappings/{id}/
- DELETE /api/vendor-product-mappings/{id}/

### Product Course Mapping
- GET /api/product-course-mappings/
- POST /api/product-course-mappings/
- GET /api/product-course-mappings/{id}/
- PUT /api/product-course-mappings/{id}/
- PATCH /api/product-course-mappings/{id}/
- DELETE /api/product-course-mappings/{id}/

### Course Certification Mapping
- GET /api/course-certification-mappings/
- POST /api/course-certification-mappings/
- GET /api/course-certification-mappings/{id}/
- PUT /api/course-certification-mappings/{id}/
- PATCH /api/course-certification-mappings/{id}/
- DELETE /api/course-certification-mappings/{id}/

## Filtering Examples
- GET /api/products/?vendor_id=1
- GET /api/courses/?product_id=2
- GET /api/certifications/?course_id=3
- GET /api/vendor-product-mappings/?vendor_id=1
- GET /api/product-course-mappings/?product_id=2
- GET /api/course-certification-mappings/?course_id=3

## Validation Rules Implemented
- Required field validation
- Unique code in master entities
- Duplicate mapping prevention
- Valid foreign key usage through serializer PK validation
- Only one primary mapping per parent at each mapping level

## Sample Request Bodies
### Create Vendor
```json
{
  "name": "Vendor A",
  "code": "VEN001",
  "description": "Main vendor",
  "is_active": true
}
```

### Create Vendor-Product Mapping
```json
{
  "vendor": 1,
  "product": 1,
  "primary_mapping": true,
  "is_active": true
}
```

## Seed Sample Data
This project includes a very basic seed command.

Run:

```bash
python manage.py seed_data
```

What it does:
- creates 2 vendors
- creates 2 products
- creates 2 courses
- creates 2 certifications
- creates mapping records between them
