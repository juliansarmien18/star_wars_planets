from rest_framework import serializers

from planets.models import Climate, Planet, Terrain


class PlanetSerializer(serializers.ModelSerializer):
    climates = serializers.ListField(
        child=serializers.CharField(), required=False, write_only=True
    )
    terrains = serializers.ListField(
        child=serializers.CharField(), required=False, write_only=True
    )
    population = serializers.CharField(allow_null=True, required=False)

    class Meta:
        model = Planet
        fields = ["name", "population", "climates", "terrains"]

    def create(self, validated_data):
        climate_names = validated_data.pop("climates", [])
        terrain_names = validated_data.pop("terrains", [])

        try:
            planet, created = Planet.objects.get_or_create(
                name=validated_data["name"],
                defaults={"population": validated_data.get("population")},
            )

            if not created:
                planet.population = validated_data.get("population")
                planet.save()

            if climate_names:
                climates = []
                for c in climate_names:
                    if c and c.strip():
                        climate, _ = Climate.objects.get_or_create(name=c.strip())
                        climates.append(climate)
                planet.climates.set(climates)

            if terrain_names:
                terrains = []
                for t in terrain_names:
                    if t and t.strip():
                        terrain, _ = Terrain.objects.get_or_create(name=t.strip())
                        terrains.append(terrain)
                planet.terrains.set(terrains)

            return planet
        except Exception as e:
            raise Exception(f"Error creating planet: {str(e)}")

    def update(self, instance, validated_data):
        climate_names = validated_data.pop("climates", None)
        terrain_names = validated_data.pop("terrains", None)

        try:
            instance.name = validated_data.get("name", instance.name)
            instance.population = validated_data.get("population", instance.population)
            instance.save()

            if climate_names is not None:
                climates = []
                for c in climate_names:
                    if c and c.strip():
                        climate, _ = Climate.objects.get_or_create(name=c.strip())
                        climates.append(climate)
                instance.climates.set(climates)

            if terrain_names is not None:
                terrains = []
                for t in terrain_names:
                    if t and t.strip():
                        terrain, _ = Terrain.objects.get_or_create(name=t.strip())
                        terrains.append(terrain)
                instance.terrains.set(terrains)

            return instance
        except Exception as e:
            raise Exception(f"Error updating planet: {str(e)}")

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        try:
            if hasattr(instance, "climates") and instance.climates:
                rep["climates"] = [c.name for c in instance.climates.all()]
            else:
                rep["climates"] = []

            if hasattr(instance, "terrains") and instance.terrains:
                rep["terrains"] = [t.name for t in instance.terrains.all()]
            else:
                rep["terrains"] = []
        except Exception as e:
            rep["climates"] = []
            rep["terrains"] = []
        return rep
