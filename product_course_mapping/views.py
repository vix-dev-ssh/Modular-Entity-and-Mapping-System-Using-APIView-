from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from product_course_mapping.models import ProductCourseMapping
from product_course_mapping.serializers import ProductCourseMappingSerializer


class ProductCourseMappingListCreateAPIView(APIView):
	@swagger_auto_schema(
		operation_description="List product-course mappings. Optional filters: product_id, course_id, primary_mapping, is_active",
		manual_parameters=[
			openapi.Parameter("product_id", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
			openapi.Parameter("course_id", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
			openapi.Parameter("primary_mapping", openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
			openapi.Parameter("is_active", openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
		],
		responses={200: ProductCourseMappingSerializer(many=True)},
	)
	def get(self, request):
		queryset = ProductCourseMapping.objects.select_related("product", "course").all().order_by("id")

		product_id = request.query_params.get("product_id")
		course_id = request.query_params.get("course_id")
		primary_mapping = request.query_params.get("primary_mapping")
		is_active = request.query_params.get("is_active")

		if product_id:
			queryset = queryset.filter(product_id=product_id)
		if course_id:
			queryset = queryset.filter(course_id=course_id)
		if primary_mapping is not None:
			queryset = queryset.filter(primary_mapping=primary_mapping.lower() == "true")
		if is_active is not None:
			queryset = queryset.filter(is_active=is_active.lower() == "true")

		serializer = ProductCourseMappingSerializer(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@swagger_auto_schema(
		operation_description="Create product-course mapping",
		request_body=ProductCourseMappingSerializer,
		responses={201: ProductCourseMappingSerializer, 400: "Validation error"},
	)
	def post(self, request):
		serializer = ProductCourseMappingSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCourseMappingDetailAPIView(APIView):
	def get_object(self, pk):
		try:
			return ProductCourseMapping.objects.get(pk=pk)
		except ProductCourseMapping.DoesNotExist:
			return None

	@swagger_auto_schema(
		operation_description="Retrieve product-course mapping",
		responses={200: ProductCourseMappingSerializer, 404: "Not found"},
	)
	def get(self, request, pk):
		mapping = self.get_object(pk)
		if not mapping:
			return Response({"detail": "Product-course mapping not found."}, status=status.HTTP_404_NOT_FOUND)
		serializer = ProductCourseMappingSerializer(mapping)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@swagger_auto_schema(
		operation_description="Update product-course mapping",
		request_body=ProductCourseMappingSerializer,
		responses={200: ProductCourseMappingSerializer, 400: "Validation error", 404: "Not found"},
	)
	def put(self, request, pk):
		mapping = self.get_object(pk)
		if not mapping:
			return Response({"detail": "Product-course mapping not found."}, status=status.HTTP_404_NOT_FOUND)

		serializer = ProductCourseMappingSerializer(mapping, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@swagger_auto_schema(
		operation_description="Partially update product-course mapping",
		request_body=ProductCourseMappingSerializer,
		responses={200: ProductCourseMappingSerializer, 400: "Validation error", 404: "Not found"},
	)
	def patch(self, request, pk):
		mapping = self.get_object(pk)
		if not mapping:
			return Response({"detail": "Product-course mapping not found."}, status=status.HTTP_404_NOT_FOUND)

		serializer = ProductCourseMappingSerializer(mapping, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@swagger_auto_schema(
		operation_description="Delete product-course mapping",
		responses={204: "Deleted", 404: "Not found"},
	)
	def delete(self, request, pk):
		mapping = self.get_object(pk)
		if not mapping:
			return Response({"detail": "Product-course mapping not found."}, status=status.HTTP_404_NOT_FOUND)
		mapping.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
