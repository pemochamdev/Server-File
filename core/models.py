from django.db import models
from usersauths.models import CustomUser
import uuid

class FileMeta(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    filename = models.CharField(max_length=255)
    chunk_number = models.IntegerField()
    total_chunks = models.IntegerField()
    uploaded_chunks = models.IntegerField(default=0)
    chunks_processed = models.IntegerField(default=0)
    folder_path = models.CharField(max_length=255)
    is_complete =models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='initializing')
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.filename


class UploadeFile(models.Model):
  id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
  author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='uploadefile')
  file_name = models.CharField(max_length=255)
  file_path = models.CharField(max_length=512)
  uploaded_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
      return str(self.file_name)
    

