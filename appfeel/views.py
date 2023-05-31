from rest_framework import viewsets
from django.shortcuts import render
from django.http import JsonResponse
from feel.settings import OPEN_AI_KEY
from django.views.decorators.csrf import csrf_exempt
import openai

openai.api_key = OPEN_AI_KEY

from .models import CustomUser
from .serializers import UserSerializer

#rest full class
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


def hello_world(request):
    return JsonResponse({'message': 'Hello, World!'})

@csrf_exempt
def generate_text(request):
    if request.method == "POST":
        data = request.POST
        prompt = data.get("message")
        response = openai.Completion.create(
            engine="davinci", prompt=prompt, max_tokens=1024)
        return JsonResponse({"message": response.choices[0].text})
    else:
        return JsonResponse({"error": "Invalid request method"})
    


