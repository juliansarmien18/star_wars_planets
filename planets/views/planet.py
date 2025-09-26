import os

import requests
from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from planets.decorators import api_response_handler
from planets.models import Planet
from planets.serializers import PlanetSerializer


class PlanetViewSet(viewsets.ModelViewSet):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @transaction.atomic
    def perform_create(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            raise Exception(f"Error creating planet: {str(e)}")

    @transaction.atomic
    def perform_update(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            raise Exception(f"Error updating planet: {str(e)}")

    @action(detail=False, methods=["GET"], url_path="sync")
    @api_response_handler
    def sync_from_swapi(self, request):
        url = os.getenv("SWAPI_PLANETS_URL")
        if not url:
            raise Exception("SWAPI_PLANETS_URL not set in .env")

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Request to SWAPI failed: {str(e)}")

        data = response.json().get("data", {}).get("allPlanets", {}).get("planets", [])

        with transaction.atomic():
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
                else:
                    print(f"Validation errors for {item['name']}: {serializer.errors}")

            return {"message": f"{created} planets imported or updated."}
