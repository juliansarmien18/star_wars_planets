from rest_framework import serializers

from planets.models import Terrain


class TerrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terrain
        fields = ["name"]
