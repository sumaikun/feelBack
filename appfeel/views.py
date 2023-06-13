from rest_framework import viewsets
from django.shortcuts import render
from django.http import JsonResponse
from feel.settings import OPEN_AI_KEY
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
import openai

#rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

openai.api_key = OPEN_AI_KEY

from .models import CustomUser
from .serializers import UserSerializer, LoginSerializer

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


class LoginView(APIView):
    def post(self, request):
        print("on login request")
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)