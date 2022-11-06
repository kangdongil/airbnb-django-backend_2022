from rest_framework.serializers import ModelSerializer
from .models import Review
from users.serializers import TinyUserSerializer

class ReviewSerializer(ModelSerializer):
    
    user = TinyUserSerializer(read_only=True)
    
    class Meta:
        model=Review
        fields = (
            "user",
            "payload",
            "rating",
            "created_at",
        )