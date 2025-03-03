from django.urls import path
from .views import chat_view, get_ai_response

urlpatterns = [
    path("", chat_view, name="chat_url"),  # Chat page
    path("api/", get_ai_response, name="chat_api"),  # API for AI responses
]