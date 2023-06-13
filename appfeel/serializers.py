from rest_framework import serializers
from .models import CustomUser, Message, Conversation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'role', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'conversation', 'user', 'content', 'created_at')

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ('id', 'room_name', 'anonymous_name', 'anonymous_email', 'anonymous_phone', 'created_at', 'messages')

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()