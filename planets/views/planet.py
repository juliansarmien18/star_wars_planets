import os

import requests
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from planets.models import Planet
from planets.serializers import PlanetSerializer


class PlanetViewSet(viewsets.ModelViewSet):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=False, methods=["GET"], url_path="sync")
    def sync_from_swapi(self, request):
        url = os.getenv("SWAPI_PLANETS_URL")
        if not url:
            return Response(
                {"detail": "SWAPI_PLANETS_URL not set in .env"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            return Response(
                {"detail": f"Request to SWAPI failed: {str(e)}"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        data = response.json().get("data", {}).get("allPlanets", {}).get("planets", [])
        created = 0
        for item in data:
            planet_data = {
                "name": item["name"],
                "population": (
                    item["population"]
                    if item["population"] not in [None, "unknown"]
                    else None
                ),
                "climates": item.get("climates") or [],
                "terrains": item.get("terrains") or [],
            }
            serializer = PlanetSerializer(data=planet_data)
            if serializer.is_valid():
                serializer.save()
                created += 1

        return Response(
            {"message": f"{created} planets imported or updated."},
            status=status.HTTP_200_OK,
        )
