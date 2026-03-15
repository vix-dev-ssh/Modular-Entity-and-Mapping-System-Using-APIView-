from django.db import models


class CourseCertificationMapping(models.Model):
	course = models.ForeignKey("course.Course", on_delete=models.CASCADE, related_name="course_certification_mappings")
	certification = models.ForeignKey(
		"certification.Certification", on_delete=models.CASCADE, related_name="course_certification_mappings"
	)
	primary_mapping = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=["course", "certification"], name="unique_course_certification_mapping")
		]

	def __str__(self):
		return f"Course {self.course_id} -> Certification {self.certification_id}"
