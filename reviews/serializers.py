from rest_framework import serializers
from .models import Review
from users.serializers import TinyUserSerializer

class ReviewSerializer(serializers.ModelSerializer):
    
    user = TinyUserSerializer(read_only=True)
    
    class Meta:
        model=Review
        fields = (
            "user",
            "payload",
            "rating",
        )