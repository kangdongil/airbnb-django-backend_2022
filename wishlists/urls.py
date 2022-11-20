from django.urls import path
from . import views


urlpatterns = [
    path("", views.WishlistList.as_view()),
    path("<int:pk>", views.WishlistDetail.as_view()),
    path("<int:pk>/rooms/<int:room_pk>", views.WishlistRoomToggle.as_view()),
    path("<int:pk>/experiences/<int:experience_pk>", views.WishlistExperienceToggle.as_view()),
]