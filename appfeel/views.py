from .serializers import UserSerializer, LoginSerializer
from .models import CustomUser
from rest_framework import viewsets
from django.shortcuts import render
from django.http import JsonResponse
from feel.settings import OPEN_AI_KEY
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
import openai

# rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view

openai.api_key = OPEN_AI_KEY


# rest full class

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


@api_view(['GET'])
def validate_token(_, token):
    try:
        #print("validating token", token)
        token_obj = Token.objects.get(key=token)
        user = token_obj.user

        if user.is_active:
            return Response({'valid': True}, status=status.HTTP_200_OK)
        else:
            return Response({'valid': False, 'message': 'User is not active.'}, status=status.HTTP_401_UNAUTHORIZED)

    except Token.DoesNotExist:
        return Response({'valid': False, 'message': 'Invalid token.'}, status=status.HTTP_404_NOT_FOUND)
