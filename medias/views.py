from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, NotAuthenticated, PermissionDenied
from rest_framework import status
from rest_framework.response import Response
from .models import Photo, Video

class PhotoDetail(APIView):
    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound
    
    def delete(self, request, pk):
        photo = self.get_object(pk)
        if not request.user.is_authenticated:
            return NotAuthenticated
        if (photo.room and photo.room.owner != request.user
            ) or (photo.experience and photo.experience.host != request.user
        ):
            raise PermissionDenied
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VideoDetail(APIView):
    pass