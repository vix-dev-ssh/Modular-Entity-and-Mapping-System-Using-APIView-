from django.core.management.base import BaseCommand

from certification.models import Certification
from course.models import Course
from course_certification_mapping.models import CourseCertificationMapping
from product.models import Product
from product_course_mapping.models import ProductCourseMapping
from vendor.models import Vendor
from vendor_product_mapping.models import VendorProductMapping


class Command(BaseCommand):
    help = "Insert simple sample data for master entities and mappings"

    def handle(self, *args, **options):
        vendor_a, _ = Vendor.objects.get_or_create(
            code="VEN001",
            defaults={
                "name": "Vendor A",
                "description": "Sample vendor A",
                "is_active": True,
            },
        )
        vendor_b, _ = Vendor.objects.get_or_create(
            code="VEN002",
            defaults={
                "name": "Vendor B",
                "description": "Sample vendor B",
                "is_active": True,
            },
        )

        product_a, _ = Product.objects.get_or_create(
            code="PROD001",
            defaults={
                "name": "Product A",
                "description": "Sample product A",
                "is_active": True,
            },
        )
        product_b, _ = Product.objects.get_or_create(
            code="PROD002",
            defaults={
                "name": "Product B",
                "description": "Sample product B",
                "is_active": True,
            },
        )

        course_a, _ = Course.objects.get_or_create(
            code="CRS001",
            defaults={
                "name": "Course A",
                "description": "Sample course A",
                "is_active": True,
            },
        )
        course_b, _ = Course.objects.get_or_create(
            code="CRS002",
            defaults={
                "name": "Course B",
                "description": "Sample course B",
                "is_active": True,
            },
        )

        certification_a, _ = Certification.objects.get_or_create(
            code="CERT001",
            defaults={
                "name": "Certification A",
                "description": "Sample certification A",
                "is_active": True,
            },
        )
        certification_b, _ = Certification.objects.get_or_create(
            code="CERT002",
            defaults={
                "name": "Certification B",
                "description": "Sample certification B",
                "is_active": True,
            },
        )

        VendorProductMapping.objects.get_or_create(
            vendor=vendor_a,
            product=product_a,
            defaults={"primary_mapping": True, "is_active": True},
        )
        VendorProductMapping.objects.get_or_create(
            vendor=vendor_b,
            product=product_b,
            defaults={"primary_mapping": True, "is_active": True},
        )

        ProductCourseMapping.objects.get_or_create(
            product=product_a,
            course=course_a,
            defaults={"primary_mapping": True, "is_active": True},
        )
        ProductCourseMapping.objects.get_or_create(
            product=product_b,
            course=course_b,
            defaults={"primary_mapping": True, "is_active": True},
        )

        CourseCertificationMapping.objects.get_or_create(
            course=course_a,
            certification=certification_a,
            defaults={"primary_mapping": True, "is_active": True},
        )
        CourseCertificationMapping.objects.get_or_create(
            course=course_b,
            certification=certification_b,
            defaults={"primary_mapping": True, "is_active": True},
        )

        self.stdout.write(self.style.SUCCESS("Sample data inserted (or already exists)."))
