from app.models import *
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "profile_picture",
            "city",
            "state",
            "country",
            "job",
            "pin",
            "phone_number",
            "facebook",
            "instagram",
            "twitter",
        )

class ProfileLikeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = ProfileLike
        fields = ("id", "user", "profile", "created_at", "updated_at")

    
class ProfileFollowerSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = ProfileFollower
        fields = ("id", "user", "profile", "created_at", "updated_at")

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ("id", "picture", "brand", "model", "year", "seats", "description", "price")

class ApplicationSerializer(serializers.ModelSerializer):
    car = serializers.SlugRelatedField(slug_field='brand', read_only=True)
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Application
        fields = ("id", "car", "start_date", "end_date", "user")
