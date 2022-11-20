from django.db import transaction
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, PermissionDenied, ParseError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.response import Response
from .models import Experience, Perk
from .serializers import ExperienceListSerializer, ExperienceDetailSerializer, PerkSerializer
from common.paginations import ListPagination, MonthlyBookingPagination
from categories.models import Category
from bookings.models import Booking
from experiences.models import Experience
from medias.models import Photo, Video
from bookings.serializers import PublicBookingSerializer, PrivateBookingSerializer, CreateExperienceBookingSerializer
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer, VideoSerializer

class PerkList(APIView, ListPagination):
    
    def get(self, request):
        all_perks = Perk.objects.all().order_by("-created_at")
        serializer = PerkSerializer(
            self.paginate(all_perks, request),
            many=True,
        )
        return Resonse({
            "page": self.paginated_info,
            "content": serializer.data,
        })

    def post(self, request):
        serializer = PerkSerializer(
            data=request.data
        )
        if serializer.is_valid():
            new_perk = serializer.save()
            serializer = PerkSerializer(new_perk)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

class PerkDetail(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk)
        return Response(serializer.data)
    
    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(
            perk,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_perk = serializer.save()
            serializer = PerkSerializer(updated_perk)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errros,
                status=status.HTTP_400_BAD_REQUEST,
            )
    
    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExperienceList(APIView, ListPagination):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_experiences = Experience.objects.all().order_by("-created_at")
        serializer = ExperienceListSerializer(
            self.paginate(all_experiences, request),
            many=True,
            context={"request": request},
        )
        return Response({
            "page": self.paginated_info,
            "content": serializer.data,
        })

    def post(self, request):
        serializer = ExperienceDetailSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            perk_pks = request.data.get("perks")
            if not category_pk:
                raise ParseError("Category is required.")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind != Category.CategoryKindChoices.EXPERIENCE:
                    raise ParseError("The category's kind should be 'experience'.")
            except Category.DoesNotExist:
                raise ParseError("Category not found.")
            try:
                with transaction.atomic():
                    new_experience = serializer.save(
                        host=request.user,
                        category=category,
                    )
                    if perk_pks:
                        for perk_pk in perk_pks:
                            perk = Perk.objects.get(pk=perk_pk)
                            new_experience.perks.add(perk)
            except Perk.DoesNotExist:
                raise ParseError("Perk not found.")
            except Exception as e:
                raise ParseError(e)
            serializer = ExperienceDetailSerializer(
                new_experience,
                context={"request": request},
            )
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class ExperienceDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = ExperienceDetailSerializer(
            experience,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        experience = self.get_object(pk)
        serializer = ExperienceDetailSerializer(
            experience,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid():
            category_pk = request.data.get("category")
            perk_pks = request.data.get("perks")
            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                except Category.DoesNotExist:
                    raise ParseError("Category not found.")
            try:
                with transaction.atomic():
                    if category_pk:
                        updated_experience = serializer.save(category=category)
                    else:
                        updated_experience = serializer.save()
                    if perk_pks:
                        updated_experience.perks.clear()
                        for perk_pk in perk_pks:
                            perk = Perk.objects.get(pk=perk_pk)
                            updated_experience.perks.add(perk)
            except Perk.DoesNotExist:
                raise ParseError("Perk not found.")
            except Exception as e:
                raise ParseError(e)

            serializer = ExperienceDetailSerializer(
                updated_experience,
                context={"request": request},
            )
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise PermissionDenied
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExperiencePerks(APIView, ListPagination):

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound
    
    def get(self, request, pk):
        experience = self.get_object(pk)
        perks = experience.perks.all()
        serializer = PerkSerializer(
            self.paginated(perks, request),
            many=True,
        )
        return Response({
            "page": self.paginated_info,
            "content": serializer.data,
        })


class ExperienceBookings(APIView, MonthlyBookingPagination):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound
    
    def get(self, request, pk):
        experience = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        is_active = request.query_params.get("active", None)
        if request.user == experience.host:
            if is_active == "true":
                bookings = Booking.objects.filter(
                    experience=experience,
                    kind=Booking.BookingKindChoices.EXPERIENCE,
                    experience_time__gte=now,
                )
            else:
                bookings = Booking.objects.filter(
                    experience=experience,
                    kind=Booking.BookingKindChoices.EXPERIENCE,
                )
            serializer = PrivateBookingSerializer(
                self.paginate(bookings, request),
                many=True,
            )
        else:
            if is_active:
                raise PermissionDenied
            bookings = Booking.objects.filter(
                experience=experience,
                kind=Booking.BookingKindChoices.EXPERIENCE,
                experience_time__gte=now,
            )
            serializer = PublicBookingSerializer(
                self.paginate(bookings, request),
                many=True,
            )
        return Response({
            "page": self.paginated_info,
            "content": serializer.data,
        })

    def post(self, request, pk):
        experience = self.get_object(pk)
        serializer = CreateExperienceBookingSerializer(
            data=request.data,
            context={"experience": experience},
        )
        if serializer.is_valid():
            new_booking = serializer.save(
                experience=experience,
                user=request.user,
                kind=Booking.BookingKindChoices.EXPERIENCE,
            )
            serializer = PublicBookingSerializer(new_booking)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class ExperienceReviews(APIView, ListPagination):

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound
    
    def get(self, request, pk):
        experience = self.get_object(pk)
        reviews = experience.reviews.all()
        serializer = ReviewSerializer(
            self.paginate(reviews, request),
            many=True,
        )
        return Response({
            "page": self.paginated_info,
            "content": serializer.data,
        })


class ExperiencePhotos(APIView, ListPagination):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        photos = experience.photos.all()
        serializer = PhotoSerializer(
            self.paginate(photos,request),
            many=True,
        )
        return Response(serializer.data)
    
    def post(self, request, pk):
        experience = self.get_object(pk)
        if request.user != experience.host:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(experience=experience)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class ExperienceThumbnailPhotoSelect(APIView):

    permission_classes = [IsAuthenticated]

    def get_experience(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get_photo(self, experience_pk, photo_pk):
        try:
            return Photo.objects.get(pk=photo_pk, experience=experience_pk)
        except Photo.DoesNotExist:
            raise NotFound

    def put(self, request, pk, photo_pk):
        experience = self.get_experience(pk)
        if experience.host != request.user:
            raise PermissionDenied
        photo = self.get_photo(pk, photo_pk)
        experience_photos = Photo.objects.filter(experience=experience)\
            .order_by("-created_at")
        thumbnail_photo = experience_photos.filter(is_thumbnail=True)
        if photo.is_thumbnail:
            raise ParseError("This photo is already a thumbnail.")
        for a_photo in thumbnail_photo:
            a_photo.is_thumbnail = False
            a_photo.save()
        photo.is_thumbnail = True
        photo.save()
        return Response(status=status.HTTP_200_OK)


class ExperienceVideo(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get_experience_video(self, experience_pk):
        try:
            video = Video.objects.filter(experience=experience_pk).first()
            return video
        except Video.DoesNotExist:
            return

    def get(self, request, pk):
        experience = self.get_object(pk)
        if not self.get_experience_video(pk):
            return Response(status=status.HTTP_200_OK)
        serializer = VideoSerializer(experience.video)
        return Response(serializer.data)

    def post(self, request, pk):
        experience = self.get_object(pk)
        if request.user != experience.host:
            raise PermissionDenied
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            if self.get_experience_video(pk):
                raise ParseError("Video with this Experience already exists.")
            video = serializer.save(experience=experience)
            serializer = VideoSerializer(video)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )