from django.urls import path
from .views import *

urlpatterns = [
    path("", product_list_view, name="shop_url"),
    path("api/products", ProductListView.as_view()),
    path("api/products/details/<pk>", ProductDetailView.as_view()),
    path("api/products/create", ProductCreateView.as_view()),
    path("category/<slug>", category_details_view),
    path("<slug>", product_details_view),

    # ✅ New FAQ and Policies URLs
    path("faq/", faq_page, name="faq_page"),
    path("policies/", policies_page, name="policies_page"),
]