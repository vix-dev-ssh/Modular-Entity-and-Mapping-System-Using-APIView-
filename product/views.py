from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product
from product.serializers import ProductSerializer
from vendor_product_mapping.models import VendorProductMapping


class ProductListCreateAPIView(APIView):
	@swagger_auto_schema(
		operation_description="List products. Optional filter: vendor_id, is_active",
		manual_parameters=[
			openapi.Parameter("vendor_id", openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
			openapi.Parameter("is_active", openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
		],
		responses={200: ProductSerializer(many=True)},
	)
	def get(self, request):
		queryset = Product.objects.all().order_by("id")

		vendor_id = request.query_params.get("vendor_id")
		is_active = request.query_params.get("is_active")

		if vendor_id:
			product_ids = VendorProductMapping.objects.filter(vendor_id=vendor_id, is_active=True).values_list(
				"product_id", flat=True
			)
			queryset = queryset.filter(id__in=product_ids)

		if is_active is not None:
			queryset = queryset.filter(is_active=is_active.lower() == "true")

		serializer = ProductSerializer(queryset.distinct(), many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@swagger_auto_schema(
		operation_description="Create a product",
		request_body=ProductSerializer,
		responses={201: ProductSerializer, 400: "Validation error"},
	)
	def post(self, request):
		serializer = ProductSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPIView(APIView):
	def get_object(self, pk):
		try:
			return Product.objects.get(pk=pk)
		except Product.DoesNotExist:
			return None

	@swagger_auto_schema(operation_description="Retrieve product", responses={200: ProductSerializer, 404: "Not found"})
	def get(self, request, pk):
		product = self.get_object(pk)
		if not product:
			return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
		serializer = ProductSerializer(product)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@swagger_auto_schema(
		operation_description="Update product",
		request_body=ProductSerializer,
		responses={200: ProductSerializer, 400: "Validation error", 404: "Not found"},
	)
	def put(self, request, pk):
		product = self.get_object(pk)
		if not product:
			return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

		serializer = ProductSerializer(product, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@swagger_auto_schema(
		operation_description="Partially update product",
		request_body=ProductSerializer,
		responses={200: ProductSerializer, 400: "Validation error", 404: "Not found"},
	)
	def patch(self, request, pk):
		product = self.get_object(pk)
		if not product:
			return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

		serializer = ProductSerializer(product, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@swagger_auto_schema(operation_description="Delete product", responses={204: "Deleted", 404: "Not found"})
	def delete(self, request, pk):
		product = self.get_object(pk)
		if not product:
			return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
		product.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
