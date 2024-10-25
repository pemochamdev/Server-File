from django.urls import path
from .views import InitializeUploadView, UploadChunkView,UserCreationView,CustomTokenObtainPairView

urlpatterns = [
    
    path('api/initialize-upload/', InitializeUploadView.as_view(), name='initialize_upload'),
    path('create-user', UserCreationView.as_view(), name='user-cration'),
    path('api/upload-chunk/<str:upload_id>/', UploadChunkView.as_view(), name='upload_chunk'),
    path('token/', CustomTokenObtainPairView.as_view(),name='my_token_pair'),
]
