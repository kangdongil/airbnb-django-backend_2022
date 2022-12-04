from django.urls import path
from . import views

urlpatterns = [
    path("rooms/", views.CategoryRoomList.as_view()),
    path("experience/", views.CategoryExperienceList.as_view()),
]