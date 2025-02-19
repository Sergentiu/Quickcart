from django.contrib import admin
from .models import Product, Category

@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "price", "category")
    prepopulated_fields = {"slug": ("name",)}