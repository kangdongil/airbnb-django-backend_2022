from django.urls import path
from . import views


urlpatterns = [
    path("", views.CreateAccount.as_view()),
    path("me", views.MyProfile.as_view()),
    path("@<str:username>", views.PublicProfile.as_view()),
    path("@<str:username>/reviews", views.UserReviews.as_view()),
    path("@<str:username>/rooms", views.HostRooms.as_view()),
    path("@<str:username>/rooms/reviews", views.HostRoomReviews.as_view()),
    path("@<str:username>/experiences", views.HostExperiences.as_view()),
    path("@<str:username>/experiences/reviews", views.HostExperienceReviews.as_view()),
    path("change-password", views.ChangePassword.as_view()),
    path("log-in", views.LogIn.as_view()),
    path("github", views.GithubLogin.as_view()),
    path("log-out", views.LogOut.as_view()),
]