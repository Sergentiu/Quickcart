from django.shortcuts import render
from .models import Product, Category, FAQ, Policy  # Added FAQ and Policy
from cart.forms import AddToCartForm
from rest_framework import generics
from .serializers import ProductSerializer
from django.contrib.auth.decorators import login_required

@login_required
def product_list_view(request):
    products = Product.objects.all()  # Get all products
    context = {
        'products': products,
    }

    return render(request, "product_list.html", context)

@login_required
def product_details_view(request, slug):
    product = Product.objects.filter(slug=slug).first()  # Get product by slug
    add_to_cart_form = AddToCartForm()  # Cart form for adding items
    context = {
        'product': product,
        'add_form': add_to_cart_form,
    }
    
    return render(request, "product_details.html", context)

@login_required
def category_details_view(request, slug):
    category = Category.objects.filter(slug=slug).first()  # Get category by slug
    products = Product.objects.filter(category=category)  # Get products by category
    context = {
        'category': category,
        'products': products,
    }

    return render(request, "category_details.html", context)

# ✅ New views for FAQs and Policies - fixed for flat structure

def faq_page(request):
    faqs = FAQ.objects.all()
    return render(request, 'faq_page.html', {'faqs': faqs})  # No 'shop/' prefix anymore

def policies_page(request):
    policies = Policy.objects.all()
    return render(request, 'policies_page.html', {'policies': policies})  # No 'shop/' prefix anymore

# REST API Views (unchanged)
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer