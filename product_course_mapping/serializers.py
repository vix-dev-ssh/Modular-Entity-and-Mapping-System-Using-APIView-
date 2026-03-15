from rest_framework import serializers

from course.models import Course
from product.models import Product
from product_course_mapping.models import ProductCourseMapping


class ProductCourseMappingSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.filter(is_active=True))
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.filter(is_active=True))

    class Meta:
        model = ProductCourseMapping
        fields = [
            "id",
            "product",
            "course",
            "primary_mapping",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        product = attrs.get("product", getattr(self.instance, "product", None))
        course = attrs.get("course", getattr(self.instance, "course", None))
        primary_mapping = attrs.get("primary_mapping", getattr(self.instance, "primary_mapping", False))

        duplicate_qs = ProductCourseMapping.objects.filter(product=product, course=course)
        if self.instance:
            duplicate_qs = duplicate_qs.exclude(id=self.instance.id)

        if duplicate_qs.exists():
            raise serializers.ValidationError("This product-course mapping already exists.")

        if primary_mapping:
            primary_qs = ProductCourseMapping.objects.filter(product=product, primary_mapping=True)
            if self.instance:
                primary_qs = primary_qs.exclude(id=self.instance.id)
            if primary_qs.exists():
                raise serializers.ValidationError(
                    "This product already has a primary course mapping."
                )

        return attrs
