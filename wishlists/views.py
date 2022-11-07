from django.db import transaction
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Wishlist
from .serializers import WishlistSerializer
from common.paginations import ListPagination
from rooms.models import Room


class WishlistList(APIView, ListPagination):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_wishlists = Wishlist.objects.filter(owner=request.user)
        serializer = WishlistSerializer(
            self.paginate(all_wishlists, request),
            many=True,
            context={"request": request},
        )
        return Response({
            "page": self.paginated_info(),
            "content": serializer.data,
        })
    
    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            room_pks = request.data.get("rooms")
            # experience_pks = request.data.get("experiences")
            try:
                with transaction.atomic():
                    new_wishlist = serializer.save(
                        owner=request.user,
                    )
                    if room_pks:
                        for room_pk in room_pks:
                            room = Room.objects.get(pk=room_pk)
                            new_wishlist.rooms.add(room)
            except Room.DoesNotExist:
                raise ParseError("Room Not Found")
            except Exception as e:
                raise ParseError(e)
            serializer = WishlistSerializer(
                new_wishlist,
                context={"request": request})
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WishlistDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk, owner):
        try:
            return Wishlist.objects.get(pk=pk, owner=owner)
        except Wishlist.DoesNotExist:
            return NotFound

    def get(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(
            wishlist,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(
            wishlist,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            room_pks = request.data.get("rooms")
            # experience_pks = request.data.get("experiences")
            try:
                with transaction.atomic():
                    updated_wishlist = serializer.save()
                    updated_wishlist.rooms.clear()
                    # updated_wishlist.experiences.clear()
                    for room_pk in room_pks:
                        room = Room.objects.get(pk=room_pk)
                        updated_wishlist.rooms.add(room)
            except Room.DoesNotExist:
                raise ParseError("Room Not Found")
            except Exception as e:
                raise ParseError(e)

            serializer = WishlistSerializer(
                updated_wishlist,
                context={"request": request},
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        wishlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WishlistToggle(APIView):

    def get_list(self, pk, owner):
        try:
            return Wishlist.objects.get(pk=pk, owner=owner)
        except Wishlist.DoesNotExist:
            return NotFound
    
    def get_room(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            return NotFound

    def put(self, request, pk, room_pk):
        wishlist = self.get_list(pk, request.user)
        room = self.get_room(pk=room_pk)
        if wishlist.rooms.filter(pk=room.pk).exists():
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)
        return Response(status=status.HTTP_200_OK)