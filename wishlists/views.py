from django.db import transaction
from rest_framework.views import APIView
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
