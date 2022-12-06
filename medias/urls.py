from django.urls import path
from .views import PhotoDetail, GetUploadURL, VideoDetail

urlpatterns = [
    path("photos/<int:pk>", PhotoDetail.as_view()),
    path("photos/get-url", GetUploadURL.as_view()),
    path("videos/<int:pk>", VideoDetail.as_view()),
]