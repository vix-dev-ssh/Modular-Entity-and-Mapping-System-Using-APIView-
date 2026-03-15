from django.db import models


class ProductCourseMapping(models.Model):
	product = models.ForeignKey("product.Product", on_delete=models.CASCADE, related_name="product_course_mappings")
	course = models.ForeignKey("course.Course", on_delete=models.CASCADE, related_name="product_course_mappings")
	primary_mapping = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=["product", "course"], name="unique_product_course_mapping")
		]

	def __str__(self):
		return f"Product {self.product_id} -> Course {self.course_id}"
