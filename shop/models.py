from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f"/shop/category/{self.slug}"
    
    class Meta:
        verbose_name_plural = 'Categories'

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to="imaginiproduse", null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/shop/{self.slug}"
    
# New FAQ model
class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name_plural = 'FAQS'

# New Policy model
class Policy(models.Model):
    key = models.CharField(max_length=50, unique=True)  # Example keys: "return_policy", "warranty_policy"
    value = models.TextField()

    def __str__(self):
        return self.key
    
    class Meta:
        verbose_name_plural = 'Policies'