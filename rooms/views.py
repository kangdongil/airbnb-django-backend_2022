from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, PermissionDenied, ParseError
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Room, Amenity
from . import serializers
from categories.models import Category


class AmenityList(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = serializers.AmenitySerializer(
            all_amenities,
            many=True,
        )
        return Response(serializer.data)
    
    def post(self, request):
        serializer = serializers.AmenitySerializer(
            data=request.data
        )
        if serializer.is_valid():
            new_amenity = serializer.save()
            serializer = serializers.AmenitySerializer(new_amenity)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            return NotFound
    
    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = serializers.AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = serializers.AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_amenity = serializer.save()
            serializer = serializers.AmenitySerializer(updated_amenity)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomList(APIView):
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = serializers.RoomListSerializer(
            all_rooms,
            many=True,
        )
        return Response(serializer.data)
    
    def post(self, request):
        if not request.user.is_authenticated:
            raise NotAuthenticated
        serializer = serializers.RoomDetailSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            # amenity_pks
            if not category_pk:
                raise ParseError("Category is required.")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind != Category.CategoryKindChoices.ROOM:
                    raise ParseError("The category's kind should be 'room'.")
            except Category.DoesNotExist:
                raise ParseError("Category not found.")
            new_rooms = serializer.save(
                owner=request.user,
                category=category,
            )
            serializer = serializers.RoomDetailSerializer(new_rooms)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            return NotFound
    
    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = serializers.RoomDetailSerializer(room)
        return Response(serializer.data)
    
    def put(self, request, pk):
        room = self.get_object(pk=pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied
        serializer = serializers.RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            category_pk = request.data.get("category")
            # amenities_pks
            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind != Category.CategoryKindChoices.ROOM:
                        raise ParseError("The category's kind should be 'room'.")
                except Category.DoesNotExist:
                    raise ParseError("Category not found.")
                updated_room = serializer.save(category=category)
            else:
                updated_room = serializer.save()
            serializer = serializers.RoomDetailSerializer(updated_room)
            return Response(serializer.data)

    def delete(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)
