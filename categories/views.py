from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from .models import Category
from .serializers import CategorySerializer
from common.paginations import ListPagination

class CategoryRoomList(APIView, ListPagination):
    
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_categories = Category.objects.filter(
            kind=Category.CategoryKindChoices.ROOM,
        )
        serializer = CategorySerializer(
            self.paginate(all_categories, request),
            many=True,
        )
        return Response({
            "page": self.paginated_info,
            "content": serializer.data,
        })
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            new_category = serializer.save()
            serializer = CategorySerializer(new_category)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class CategoryExperienceList(APIView, ListPagination):
    
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_categories = Category.objects.filter(
            kind=Category.CategoryKindChoices.EXPERIENCE,
        )
        serializer = CategorySerializer(
            self.paginate(all_categories, request),
            many=True,
        )
        return Response({
            "page": self.paginated_info,
            "content": serializer.data,
        })
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            new_category = serializer.save()
            serializer = CategorySerializer(new_category)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )