from django.urls import path
from . import views

urlpatterns = [
    path("", views.ExperienceList.as_view()),
    path("<int:pk>", views.ExperienceDetail.as_view()),
]