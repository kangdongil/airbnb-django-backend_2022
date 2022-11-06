from rest_framework.serializers import ModelSerializer
from users.models import User
from rooms.models import Room

class TinyUserSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=(
            "username",
            "name",
            "avatar",
        )


class TinyRoomSerializer(ModelSerializer):

    class Meta:
        model=Room
        fields=(
            "pk",
            "name",
            #"preview_photo",
        )