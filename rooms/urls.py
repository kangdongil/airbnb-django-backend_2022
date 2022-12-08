from django.urls import path
from . import views

urlpatterns = [
    path("", views.RoomList.as_view()),
    path("<int:pk>", views.RoomDetail.as_view()),
    path("<int:pk>/reviews", views.RoomReviews.as_view()),
    path("<int:pk>/amenities", views.RoomAmenities.as_view()),
    path("<int:pk>/photos", views.RoomPhotos.as_view()),
    path("<int:pk>/photos/<int:photo_pk>", views.RoomThumbnailPhotoSelect.as_view()),
    path("<int:pk>/bookings", views.RoomBookings.as_view()),
    path("<int:pk>/bookings/check", views.RoomBookingCheck.as_view()),
    path("amenities/", views.AmenityList.as_view()),
    path("amenities/<int:pk>", views.AmenityDetail.as_view()),
]