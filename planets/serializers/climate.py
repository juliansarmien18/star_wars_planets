from rest_framework import serializers

from planets.models import Climate


class ClimateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Climate
        fields = ["name"]
