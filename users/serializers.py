from rest_framework.serializers import ModelSerializer
from .models import User

class TinyUserSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=(
            "name",
            "avatar",
        )


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model=User
        """
        exclude=(
            "id",
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
        )
        """
        fields=(
            "username",
            "email",
            "avatar",
            "name",
            "last_login",
            "date_joined",
            "is_host",
            "gender",
            "language",
            "currency",
        )