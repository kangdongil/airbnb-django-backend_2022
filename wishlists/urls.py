from django.urls import path
from . import views


urlpatterns = [
    path("", views.WishlistList.as_view()),
]