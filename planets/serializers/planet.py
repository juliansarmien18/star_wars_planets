from rest_framework import serializers

from planets.models import Climate, Planet, Terrain


class PlanetSerializer(serializers.ModelSerializer):
    climates = serializers.ListField(child=serializers.CharField(), required=False)
    terrains = serializers.ListField(child=serializers.CharField(), required=False)
    population = serializers.CharField(allow_null=True, required=False)

    class Meta:
        model = Planet
        fields = ["name", "population", "climates", "terrains"]

    def create(self, validated_data):
        climate_names = validated_data.pop("climates", [])
        terrain_names = validated_data.pop("terrains", [])

        planet, _ = Planet.objects.get_or_create(name=validated_data["name"])
        planet.population = validated_data.get("population") or None
        planet.save()

        # Climates
        climates = []
        for cname in climate_names:
            climate, _ = Climate.objects.get_or_create(name=cname.strip())
            climates.append(climate)
        planet.climates.set(climates)

        # Terrains
        terrains = []
        for tname in terrain_names:
            terrain, _ = Terrain.objects.get_or_create(name=tname.strip())
            terrains.append(terrain)
        planet.terrains.set(terrains)

        return planet
