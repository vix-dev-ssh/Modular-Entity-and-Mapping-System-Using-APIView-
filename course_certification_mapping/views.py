from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from course_certification_mapping.models import CourseCertificationMapping
from course_certification_mapping.serializers import CourseCertificationMappingSerializer


class CourseCertificationMappingListCreateAPIView(APIView):
	@swagger_auto_schema(
		operation_description="List course-certification mappings. Optional filters: course_id, certification_id, primary_mapping, is_active",
		manual_parameters=[
			openapi.Parameter("course_id", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
			openapi.Parameter("certification_id", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
			openapi.Parameter("primary_mapping", openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
			openapi.Parameter("is_active", openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
		],
		responses={200: CourseCertificationMappingSerializer(many=True)},
	)
	def get(self, request):
		queryset = CourseCertificationMapping.objects.select_related("course", "certification").all().order_by("id")

		course_id = request.query_params.get("course_id")
		certification_id = request.query_params.get("certification_id")
		primary_mapping = request.query_params.get("primary_mapping")
		is_active = request.query_params.get("is_active")

		if course_id:
			queryset = queryset.filter(course_id=course_id)
		if certification_id:
			queryset = queryset.filter(certification_id=certification_id)
		if primary_mapping is not None:
			queryset = queryset.filter(primary_mapping=primary_mapping.lower() == "true")
		if is_active is not None:
			queryset = queryset.filter(is_active=is_active.lower() == "true")

		serializer = CourseCertificationMappingSerializer(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@swagger_auto_schema(
		operation_description="Create course-certification mapping",
		request_body=CourseCertificationMappingSerializer,
		responses={201: CourseCertificationMappingSerializer, 400: "Validation error"},
	)
	def post(self, request):
		serializer = CourseCertificationMappingSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseCertificationMappingDetailAPIView(APIView):
	def get_object(self, pk):
		try:
			return CourseCertificationMapping.objects.get(pk=pk)
		except CourseCertificationMapping.DoesNotExist:
			return None

	@swagger_auto_schema(
		operation_description="Retrieve course-certification mapping",
		responses={200: CourseCertificationMappingSerializer, 404: "Not found"},
	)
	def get(self, request, pk):
		mapping = self.get_object(pk)
		if not mapping:
			return Response({"detail": "Course-certification mapping not found."}, status=status.HTTP_404_NOT_FOUND)
		serializer = CourseCertificationMappingSerializer(mapping)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@swagger_auto_schema(
		operation_description="Update course-certification mapping",
		request_body=CourseCertificationMappingSerializer,
		responses={200: CourseCertificationMappingSerializer, 400: "Validation error", 404: "Not found"},
	)
	def put(self, request, pk):
		mapping = self.get_object(pk)
		if not mapping:
			return Response({"detail": "Course-certification mapping not found."}, status=status.HTTP_404_NOT_FOUND)

		serializer = CourseCertificationMappingSerializer(mapping, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@swagger_auto_schema(
		operation_description="Partially update course-certification mapping",
		request_body=CourseCertificationMappingSerializer,
		responses={200: CourseCertificationMappingSerializer, 400: "Validation error", 404: "Not found"},
	)
	def patch(self, request, pk):
		mapping = self.get_object(pk)
		if not mapping:
			return Response({"detail": "Course-certification mapping not found."}, status=status.HTTP_404_NOT_FOUND)

		serializer = CourseCertificationMappingSerializer(mapping, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@swagger_auto_schema(
		operation_description="Delete course-certification mapping",
		responses={204: "Deleted", 404: "Not found"},
	)
	def delete(self, request, pk):
		mapping = self.get_object(pk)
		if not mapping:
			return Response({"detail": "Course-certification mapping not found."}, status=status.HTTP_404_NOT_FOUND)
		mapping.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
