from rest_framework import serializers

from product.models import Product
from vendor.models import Vendor
from vendor_product_mapping.models import VendorProductMapping


class VendorProductMappingSerializer(serializers.ModelSerializer):
    vendor = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.filter(is_active=True))
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.filter(is_active=True))

    class Meta:
        model = VendorProductMapping
        fields = [
            "id",
            "vendor",
            "product",
            "primary_mapping",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        vendor = attrs.get("vendor", getattr(self.instance, "vendor", None))
        product = attrs.get("product", getattr(self.instance, "product", None))
        primary_mapping = attrs.get("primary_mapping", getattr(self.instance, "primary_mapping", False))

        duplicate_qs = VendorProductMapping.objects.filter(vendor=vendor, product=product)

        if self.instance:
            duplicate_qs = duplicate_qs.exclude(id=self.instance.id)

        if duplicate_qs.exists():
            raise serializers.ValidationError("This vendor-product mapping already exists.")

        if primary_mapping:
            primary_qs = VendorProductMapping.objects.filter(vendor=vendor, primary_mapping=True)
            if self.instance:
                primary_qs = primary_qs.exclude(id=self.instance.id)
            if primary_qs.exists():
                raise serializers.ValidationError(
                    "This vendor already has a primary product mapping."
                )

        return attrs
