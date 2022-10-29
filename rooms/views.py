from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Room
from . import serializers


class RoomList(APIView):
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = serializers.RoomListSerializer(
            all_rooms,
            many=True,
        )
        return Response(serializer.data)
    
    def post(self, request):
        pass

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
        pass

    def delete(self, request, pk):
        pass