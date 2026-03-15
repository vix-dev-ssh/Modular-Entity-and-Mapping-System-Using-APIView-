from django.contrib import admin

from product.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "code", "is_active", "created_at")
	search_fields = ("name", "code")
