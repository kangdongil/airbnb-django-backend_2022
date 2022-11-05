from django.urls import path
from . import views


urlpatterns = [
    path("", views.CreateAccount.as_view()),
    path("me", views.MyProfile.as_view()),
    path("@<str:username>", views.PublicProfile.as_view()),
]