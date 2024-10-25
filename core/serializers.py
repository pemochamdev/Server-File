from rest_framework import serializers
from .models import FileMeta, UploadeFile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model,authenticate
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class FileMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileMeta
        fields = ['filename', 'total_chunks']  # N'incluez pas 'user' ici

    def create(self, validated_data):
        user = self.context['request'].user if self.context['request'].user.is_authenticated else None
        return FileMeta.objects.create(user=user, **validated_data)  

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadeFile
        fields = ['file_name', 'file_path']

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Ajoutez des claims supplémentaires si nécessaire
        return token

    @classmethod
    def validate(cls, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError('Invalid credentials')

        if not user.check_password(password):
            raise serializers.ValidationError('Invalid credentials')

        return super().validate(attrs)


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["email", "username"]

            