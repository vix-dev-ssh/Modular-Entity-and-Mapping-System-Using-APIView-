from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from course.models import Course
from course.serializers import CourseSerializer
from product_course_mapping.models import ProductCourseMapping


class CourseListCreateAPIView(APIView):
	@swagger_auto_schema(
		operation_description="List courses. Optional filter: product_id, is_active",
		manual_parameters=[
			openapi.Parameter("product_id", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
			openapi.Parameter("is_active", openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
		],
		responses={200: CourseSerializer(many=True)},
	)
	def get(self, request):
		queryset = Course.objects.all().order_by("id")

		product_id = request.query_params.get("product_id")
		is_active = request.query_params.get("is_active")

		if product_id:
			course_ids = ProductCourseMapping.objects.filter(product_id=product_id, is_active=True).values_list(
				"course_id", flat=True
			)
			queryset = queryset.filter(id__in=course_ids)

		if is_active is not None:
			queryset = queryset.filter(is_active=is_active.lower() == "true")

		serializer = CourseSerializer(queryset.distinct(), many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@swagger_auto_schema(
		operation_description="Create a course",
		request_body=CourseSerializer,
		responses={201: CourseSerializer, 400: "Validation error"},
	)
	def post(self, request):
		serializer = CourseSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailAPIView(APIView):
	def get_object(self, pk):
		try:
			return Course.objects.get(pk=pk)
		except Course.DoesNotExist:
			return None

	@swagger_auto_schema(operation_description="Retrieve course", responses={200: CourseSerializer, 404: "Not found"})
	def get(self, request, pk):
		course = self.get_object(pk)
		if not course:
			return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)
		serializer = CourseSerializer(course)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@swagger_auto_schema(
		operation_description="Update course",
		request_body=CourseSerializer,
		responses={200: CourseSerializer, 400: "Validation error", 404: "Not found"},
	)
	def put(self, request, pk):
		course = self.get_object(pk)
		if not course:
			return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

		serializer = CourseSerializer(course, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@swagger_auto_schema(
		operation_description="Partially update course",
		request_body=CourseSerializer,
		responses={200: CourseSerializer, 400: "Validation error", 404: "Not found"},
	)
	def patch(self, request, pk):
		course = self.get_object(pk)
		if not course:
			return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

		serializer = CourseSerializer(course, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@swagger_auto_schema(operation_description="Delete course", responses={204: "Deleted", 404: "Not found"})
	def delete(self, request, pk):
		course = self.get_object(pk)
		if not course:
			return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)
		course.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
