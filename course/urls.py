from django.urls import path

from course.views import CourseDetailAPIView, CourseListCreateAPIView

urlpatterns = [
    path("", CourseListCreateAPIView.as_view(), name="course-list-create"),
    path("<int:pk>/", CourseDetailAPIView.as_view(), name="course-detail"),
]
