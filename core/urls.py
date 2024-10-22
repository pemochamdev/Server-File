from django.urls import path
from .views import InitializeUploadView, UploadChunkView

urlpatterns = [
    path('api/initialize-upload/', InitializeUploadView.as_view(), name='initialize_upload'),
    path('api/upload-chunk/<str:upload_id>/', UploadChunkView.as_view(), name='upload_chunk'),
]
