from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied, ParseError
from rest_framework import status
from rest_framework.response import Response
from .models import Booking
from reviews.models import Review
from reviews.serializers import ReviewSerializer

class BookingDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        booking = self.get_object(pk)
        if (booking.room and booking.room.owner != request.user
            ) or (booking.experience and booking.experience.host != request.user
        ):
            raise PermissionDenied
        booking.is_cancelled = True
        booking.save()
        return Response(status=status.HTTP_200_OK)


class CreateReviewPerBooking(APIView):

    permission_classes = [IsAuthenticated]

    def get_booking(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            raise NotFound
    
    def get_booking_review(self, booking_pk):
        try:
            review = Review.objects.filter(booking=booking_pk).first()
            return review
        except Review.DoesNotExist:
            return
    
    def post(self, request, pk):
        now = timezone.localtime(timezone.now())
        booking = self.get_booking(pk)
        if (booking.room and booking.room.owner != request.user
            ) or (booking.experience and booking.experience.host != request.user
        ):
            raise PermissionDenied
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            if self.get_booking_review(pk):
                raise ParseError("Review with this Booking already exists.")
            if (booking.is_cancelled) or (
                booking.host_approval_state != "confirmed"
                ) or (booking.check_out and now.date() < booking.check_out
                ) or (booking.experience_time and now < booking.experience_time):
                raise ParseError("Review can be created when Booking is finished.")
            new_review = serializer.save(
                user=request.user,
                room=booking.room,
                experience=booking.experience,
                booking=booking,
            )
            serializer = ReviewSerializer(new_review)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
    
    def put(self,request, pk):
        now = timezone.localtime(timezone.now()).date()
        booking = self.get_booking(pk)
        review = self.get_booking_review(pk)
        if (booking.room and booking.room.owner != request.user
            ) or (booking.experience and booking.experience.host != request.user
        ):
            raise PermissionDenied
        if not review:
            raise ParseError("Please create a review first.")
        serializer = ReviewSerializer(
            review,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_review = serializer.save(
                user=request.user,
                booking=booking,
            )
            serializer = ReviewSerializer(updated_review)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
