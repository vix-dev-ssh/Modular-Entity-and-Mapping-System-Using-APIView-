from rest_framework import serializers

from certification.models import Certification
from course.models import Course
from course_certification_mapping.models import CourseCertificationMapping


class CourseCertificationMappingSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.filter(is_active=True))
    certification = serializers.PrimaryKeyRelatedField(queryset=Certification.objects.filter(is_active=True))

    class Meta:
        model = CourseCertificationMapping
        fields = [
            "id",
            "course",
            "certification",
            "primary_mapping",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        course = attrs.get("course", getattr(self.instance, "course", None))
        certification = attrs.get("certification", getattr(self.instance, "certification", None))
        primary_mapping = attrs.get("primary_mapping", getattr(self.instance, "primary_mapping", False))

        duplicate_qs = CourseCertificationMapping.objects.filter(course=course, certification=certification)
        if self.instance:
            duplicate_qs = duplicate_qs.exclude(id=self.instance.id)

        if duplicate_qs.exists():
            raise serializers.ValidationError("This course-certification mapping already exists.")

        if primary_mapping:
            primary_qs = CourseCertificationMapping.objects.filter(course=course, primary_mapping=True)
            if self.instance:
                primary_qs = primary_qs.exclude(id=self.instance.id)
            if primary_qs.exists():
                raise serializers.ValidationError(
                    "This course already has a primary certification mapping."
                )

        return attrs
