from rest_framework import serializers
from .models import FileMeta, UploadeFile

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