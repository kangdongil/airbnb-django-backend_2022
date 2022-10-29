from django.urls import path
from . import views

urlpatterns = [
    path("", views.CategoryList.as_view()),
    path("<int:pk>", views.CategoryDetail.as_view()),
]