import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework import status
from rest_framework.response import Response
from .models import Photo, Video

class PhotoDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound
    
    def delete(self, request, pk):
        photo = self.get_object(pk)
        if (photo.room and photo.room.owner != request.user
            ) or (photo.experience and photo.experience.host != request.user
        ):
            raise PermissionDenied
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VideoDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        video = self.get_object(pk)
        if video.experience and video.experience.host != request.user:
            raise PermissionDenied
        video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetUploadURL(APIView):

    def post(self, request):
        url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CF_ID}/images/v2/direct_upload"
        instant_url = requests.post(url, headers={
            "Authorization": f"Bearer {settings.CF_TOKEN}"
        }).json()
        result = instant_url.get("result")
        return Response({
            "uploadURL": result.get("uploadURL")
        })
