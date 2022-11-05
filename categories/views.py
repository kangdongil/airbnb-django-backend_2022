from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Category
from .serializers import CategorySerializer
from common.paginations import ListPagination

class CategoryList(APIView, ListPagination):
    
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_categories = Category.objects.all()
        serializer = CategorySerializer(
            self.paginate(all_categories, request),
            many=True,
        )
        return Response({
            "page": self.paginated_info(),
            "content": serializer.data,
        })
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            new_category = serializer.save()
            serializer = CategorySerializer(new_category)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class CategoryDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_object(self, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound
        return category

    def get(self, request, pk):
        serializer = CategorySerializer(self.get_object(pk))
        return Response(serializer.data)
    
    def put(self, request, pk):
        serializer = CategorySerializer(
            self.get_object(pk),
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_category = serializer.save()
            serializer = CategorySerializer(updated_category)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)