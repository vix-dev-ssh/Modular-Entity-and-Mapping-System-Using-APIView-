from django.urls import path

from course_certification_mapping.views import (
    CourseCertificationMappingDetailAPIView,
    CourseCertificationMappingListCreateAPIView,
)

urlpatterns = [
    path("", CourseCertificationMappingListCreateAPIView.as_view(), name="course-certification-mapping-list-create"),
    path("<int:pk>/", CourseCertificationMappingDetailAPIView.as_view(), name="course-certification-mapping-detail"),
]
