from django.http import JsonResponse
from django.shortcuts import render
import openai
import os

# Load OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_view(request):
    """Render the chat interface."""
    return render(request, 'chat.html')

def get_ai_response(request):
    """Handle AJAX requests and return AI-generated responses."""
    if request.method == "POST":
        user_input = request.POST.get("message", "")

        if not user_input:
            return JsonResponse({"error": "Message cannot be empty"}, status=400)

        try:
            # OpenAI API request
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an AI chatbot assisting customers."},
                    {"role": "user", "content": user_input}
                ]
            )
            ai_response = response["choices"][0]["message"]["content"]
            return JsonResponse({"response": ai_response})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)