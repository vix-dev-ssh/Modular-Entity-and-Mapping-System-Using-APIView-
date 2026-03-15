from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from vendor_product_mapping.models import VendorProductMapping
from vendor_product_mapping.serializers import VendorProductMappingSerializer


class VendorProductMappingListCreateAPIView(APIView):
	@swagger_auto_schema(
		operation_description="List vendor-product mappings. Optional filters: vendor_id, product_id, primary_mapping, is_active",
		manual_parameters=[
			openapi.Parameter("vendor_id", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
			openapi.Parameter("product_id", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
			openapi.Parameter("primary_mapping", openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
			openapi.Parameter("is_active", openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
		],
		responses={200: VendorProductMappingSerializer(many=True)},
	)
	def get(self, request):
		queryset = VendorProductMapping.objects.select_related("vendor", "product").all().order_by("id")

		vendor_id = request.query_params.get("vendor_id")
		product_id = request.query_params.get("product_id")
		primary_mapping = request.query_params.get("primary_mapping")
		is_active = request.query_params.get("is_active")

		if vendor_id:
			queryset = queryset.filter(vendor_id=vendor_id)
		if product_id:
			queryset = queryset.filter(product_id=product_id)
		if primary_mapping is not None:
			queryset = queryset.filter(primary_mapping=primary_mapping.lower() == "true")
		if is_active is not None:
			queryset = queryset.filter(is_active=is_active.lower() == "true")

		serializer = VendorProductMappingSerializer(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@swagger_auto_schema(
		operation_description="Create vendor-product mapping",
		request_body=VendorProductMappingSerializer,
		responses={201: VendorProductMappingSerializer, 400: "Validation error"},
	)
	def post(self, request):
		serializer = VendorProductMappingSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorProductMappingDetailAPIView(APIView):
	def get_object(self, pk):
		try:
			return VendorProductMapping.objects.get(pk=pk)
		except VendorProductMapping.DoesNotExist:
			return None

	@swagger_auto_schema(
		operation_description="Retrieve vendor-product mapping",
		responses={200: VendorProductMappingSerializer, 404: "Not found"},
	)
	def get(self, request, pk):
		mapping = self.get_object(pk)
		if not mapping:
			return Response({"detail": "Vendor-product mapping not found."}, status=status.HTTP_404_NOT_FOUND)
		serializer = VendorProductMappingSerializer(mapping)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@swagger_auto_schema(
		operation_description="Update vendor-product mapping",
		request_body=VendorProductMappingSerializer,
		responses={200: VendorProductMappingSerializer, 400: "Validation error", 404: "Not found"},
	)
	def put(self, request, pk):
		mapping = self.get_object(pk)
		if not mapping:
			return Response({"detail": "Vendor-product mapping not found."}, status=status.HTTP_404_NOT_FOUND)

		serializer = VendorProductMappingSerializer(mapping, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@swagger_auto_schema(
		operation_description="Partially update vendor-product mapping",
		request_body=VendorProductMappingSerializer,
		responses={200: VendorProductMappingSerializer, 400: "Validation error", 404: "Not found"},
	)
	def patch(self, request, pk):
		mapping = self.get_object(pk)
		if not mapping:
			return Response({"detail": "Vendor-product mapping not found."}, status=status.HTTP_404_NOT_FOUND)

		serializer = VendorProductMappingSerializer(mapping, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@swagger_auto_schema(
		operation_description="Delete vendor-product mapping",
		responses={204: "Deleted", 404: "Not found"},
	)
	def delete(self, request, pk):
		mapping = self.get_object(pk)
		if not mapping:
			return Response({"detail": "Vendor-product mapping not found."}, status=status.HTTP_404_NOT_FOUND)
		mapping.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
