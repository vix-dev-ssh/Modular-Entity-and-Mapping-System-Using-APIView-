from django.urls import path

from certification.views import CertificationDetailAPIView, CertificationListCreateAPIView

urlpatterns = [
    path("", CertificationListCreateAPIView.as_view(), name="certification-list-create"),
    path("<int:pk>/", CertificationDetailAPIView.as_view(), name="certification-detail"),
]
