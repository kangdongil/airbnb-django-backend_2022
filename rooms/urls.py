from django.urls import path
from . import views

urlpatterns = [
    path("", views.RoomList.as_view()),
    path("<int:pk>", views.RoomDetail.as_view()),
    path("amenities/", views.AmenityList.as_view()),
    path("amenities/<int:pk>", views.AmenityDetail.as_view()),
]