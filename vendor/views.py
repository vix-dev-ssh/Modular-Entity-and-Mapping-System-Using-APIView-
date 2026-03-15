from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from vendor.models import Vendor
from vendor.serializers import VendorSerializer


class VendorListCreateAPIView(APIView):
	@swagger_auto_schema(
		operation_description="List vendors. Optional filter: is_active=true/false",
		responses={200: VendorSerializer(many=True)},
	)
	def get(self, request):
		queryset = Vendor.objects.all().order_by("id")
		is_active = request.query_params.get("is_active")

		if is_active is not None:
			queryset = queryset.filter(is_active=is_active.lower() == "true")

		serializer = VendorSerializer(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@swagger_auto_schema(
		operation_description="Create a vendor",
		request_body=VendorSerializer,
		responses={201: VendorSerializer, 400: "Validation error"},
	)
	def post(self, request):
		serializer = VendorSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorDetailAPIView(APIView):
	def get_object(self, pk):
		try:
			return Vendor.objects.get(pk=pk)
		except Vendor.DoesNotExist:
			return None

	@swagger_auto_schema(operation_description="Retrieve vendor", responses={200: VendorSerializer, 404: "Not found"})
	def get(self, request, pk):
		vendor = self.get_object(pk)
		if not vendor:
			return Response({"detail": "Vendor not found."}, status=status.HTTP_404_NOT_FOUND)
		serializer = VendorSerializer(vendor)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@swagger_auto_schema(
		operation_description="Update vendor",
		request_body=VendorSerializer,
		responses={200: VendorSerializer, 400: "Validation error", 404: "Not found"},
	)
	def put(self, request, pk):
		vendor = self.get_object(pk)
		if not vendor:
			return Response({"detail": "Vendor not found."}, status=status.HTTP_404_NOT_FOUND)

		serializer = VendorSerializer(vendor, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@swagger_auto_schema(
		operation_description="Partially update vendor",
		request_body=VendorSerializer,
		responses={200: VendorSerializer, 400: "Validation error", 404: "Not found"},
	)
	def patch(self, request, pk):
		vendor = self.get_object(pk)
		if not vendor:
			return Response({"detail": "Vendor not found."}, status=status.HTTP_404_NOT_FOUND)

		serializer = VendorSerializer(vendor, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@swagger_auto_schema(operation_description="Delete vendor", responses={204: "Deleted", 404: "Not found"})
	def delete(self, request, pk):
		vendor = self.get_object(pk)
		if not vendor:
			return Response({"detail": "Vendor not found."}, status=status.HTTP_404_NOT_FOUND)
		vendor.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
