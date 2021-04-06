from rest_framework import serializers
from .models import Car


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["id", "make", "model", "rating"]

    def validate_rating(self, value):
        if value not in [0, 1, 2, 3, 4, 5]:
            raise serializers.ValidationError("Rating has to be a number 0-5.")
        else:
            return value


class CarSerializerRatingCount(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["id", "make", "model", "rating", "rating_count"]
