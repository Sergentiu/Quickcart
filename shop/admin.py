from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Category, FAQ, Policy

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'category', 'image', 'available', 'slug']  # Include slug
        exclude = []  # Remove exclude since we're handling slug explicitly

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price <= 0:
            raise ValidationError("Price must be greater than zero.")
        return price

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance'] and self.instance.pk:  # For edit pages
            self.fields['slug'].widget.attrs['readonly'] = True  # Make slug read-only on edit
        else:  # For add pages
            self.fields['slug'].required = False  # Optional on creation (prepopulated)

@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "price", "category", "image_preview")
    list_filter = ("category", "available")
    search_fields = ("name", "description")
    fields = ("name", "price", "description", "category", "image", "available", "slug", "created", "updated")
    readonly_fields = ("created", "updated")  # Remove slug from readonly if you want prepopulation
    prepopulated_fields = {"slug": ("name",)}
    list_display_links = ("name",)
    form = ProductAdminForm

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50" />'
        return "No Image"
    image_preview.short_description = "Image Preview"
    image_preview.allow_tags = True

    def formfield_for_djangofilefield(self, db_field, **kwargs):
        if db_field.name == "image":
            kwargs["widget"].attrs.update({"accept": "image/*"})
        return super().formfield_for_djangofilefield(db_field, **kwargs)

@admin.register(FAQ)
class AdminFAQ(admin.ModelAdmin):
    list_display = ("id", "question", "answer")

@admin.register(Policy)
class AdminPolicy(admin.ModelAdmin):
    list_display = ("id", "key", "value")