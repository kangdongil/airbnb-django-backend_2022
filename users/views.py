from django.db import transaction
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.response import Response
from .models import User
from .serializers import PrivateUserSerializer


class MyProfile(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request):
        user = request.user
        serializer = PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_user = serializer.save()
            serializer = PrivateUserSerializer(updated_user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PublicProfile(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return NotFound
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)


class CreateAccount(APIView):
    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError("Password is required.")
        serializer = PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    new_user = serializer.save()
                    new_user.set_password(password)
                    new_user.save()
                    serializer = PrivateUserSerializer(new_user)
                    return Response(serializer.data)
            except Exception as e:
                raise ParseError(e)
        else:
            return Response(serializer.errors)