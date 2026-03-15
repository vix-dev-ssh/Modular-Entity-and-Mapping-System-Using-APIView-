from django.db import models


class VendorProductMapping(models.Model):
	vendor = models.ForeignKey("vendor.Vendor", on_delete=models.CASCADE, related_name="vendor_product_mappings")
	product = models.ForeignKey("product.Product", on_delete=models.CASCADE, related_name="vendor_product_mappings")
	primary_mapping = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=["vendor", "product"], name="unique_vendor_product_mapping")
		]

	def __str__(self):
		return f"Vendor {self.vendor_id} -> Product {self.product_id}"
