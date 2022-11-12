from django.urls import path
from . import views

urlpatterns = [
    path("<int:pk>", views.BookingDetail.as_view()),
    path("<int:pk>/review", views.CreateReviewPerBooking.as_view()),
]