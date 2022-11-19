from django.db import transaction
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, PermissionDenied, ParseError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.response import Response
from .models import Experience, Perk
from .serializers import ExperienceListSerializer, ExperienceDetailSerializer
from common.paginations import ListPagination
from categories.models import Category


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