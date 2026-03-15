from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from certification.models import Certification
from certification.serializers import CertificationSerializer
from course_certification_mapping.models import CourseCertificationMapping


class CertificationListCreateAPIView(APIView):
	@swagger_auto_schema(
		operation_description="List certifications. Optional filter: course_id, is_active",
		manual_parameters=[
			openapi.Parameter("course_id", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
			openapi.Parameter("is_active", openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
		],
		responses={200: CertificationSerializer(many=True)},
	)
	def get(self, request):
		queryset = Certification.objects.all().order_by("id")

		course_id = request.query_params.get("course_id")
		is_active = request.query_params.get("is_active")

		if course_id:
			certification_ids = CourseCertificationMapping.objects.filter(course_id=course_id, is_active=True).values_list(
				"certification_id", flat=True
			)
			queryset = queryset.filter(id__in=certification_ids)

		if is_active is not None:
			queryset = queryset.filter(is_active=is_active.lower() == "true")

		serializer = CertificationSerializer(queryset.distinct(), many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@swagger_auto_schema(
		operation_description="Create a certification",
		request_body=CertificationSerializer,
		responses={201: CertificationSerializer, 400: "Validation error"},
	)
	def post(self, request):
		serializer = CertificationSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CertificationDetailAPIView(APIView):
	def get_object(self, pk):
		try:
			return Certification.objects.get(pk=pk)
		except Certification.DoesNotExist:
			return None

	@swagger_auto_schema(
		operation_description="Retrieve certification",
		responses={200: CertificationSerializer, 404: "Not found"},
	)
	def get(self, request, pk):
		certification = self.get_object(pk)
		if not certification:
			return Response({"detail": "Certification not found."}, status=status.HTTP_404_NOT_FOUND)
		serializer = CertificationSerializer(certification)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@swagger_auto_schema(
		operation_description="Update certification",
		request_body=CertificationSerializer,
		responses={200: CertificationSerializer, 400: "Validation error", 404: "Not found"},
	)
	def put(self, request, pk):
		certification = self.get_object(pk)
		if not certification:
			return Response({"detail": "Certification not found."}, status=status.HTTP_404_NOT_FOUND)

		serializer = CertificationSerializer(certification, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@swagger_auto_schema(
		operation_description="Partially update certification",
		request_body=CertificationSerializer,
		responses={200: CertificationSerializer, 400: "Validation error", 404: "Not found"},
	)
	def patch(self, request, pk):
		certification = self.get_object(pk)
		if not certification:
			return Response({"detail": "Certification not found."}, status=status.HTTP_404_NOT_FOUND)

		serializer = CertificationSerializer(certification, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@swagger_auto_schema(operation_description="Delete certification", responses={204: "Deleted", 404: "Not found"})
	def delete(self, request, pk):
		certification = self.get_object(pk)
		if not certification:
			return Response({"detail": "Certification not found."}, status=status.HTTP_404_NOT_FOUND)
		certification.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
