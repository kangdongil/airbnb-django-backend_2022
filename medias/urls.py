from django.urls import path
from .views import PhotoDetail, VideoDetail

urlpatterns = [
    path("photos/<int:pk>", PhotoDetail.as_view()),
    path("videos/<int:pk>", VideoDetail.as_view()),
]