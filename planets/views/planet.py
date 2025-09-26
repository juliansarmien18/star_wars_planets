import os

import requests
from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from core.utils.pagination import PlanetPagination
from planets.decorators import api_response_handler
from planets.models import Planet
from planets.serializers import PlanetSerializer


class PlanetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing planets.

    Provides CRUD operations for planets including:
    - List all planets with pagination and search
    - Retrieve specific planet details
    - Create new planets with climate and terrain associations
    - Update existing planets
    - Delete planets
    - Sync planets from external SWAPI API

    Search functionality allows filtering by planet name.
    """

    queryset = Planet.objects.all().order_by("name")
    serializer_class = PlanetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PlanetPagination
    filter_backends = [SearchFilter]
    search_fields = ["name"]

    @transaction.atomic
    def perform_create(self, serializer):
        """Create a new planet with atomic transaction."""
        try:
            serializer.save()
        except Exception as e:
            raise Exception(f"Error creating planet: {str(e)}")

    @transaction.atomic
    def perform_update(self, serializer):
        """Update an existing planet with atomic transaction."""
        try:
            serializer.save()
        except Exception as e:
            raise Exception(f"Error updating planet: {str(e)}")

    @action(detail=False, methods=["GET"], url_path="sync")
    @api_response_handler
    def sync_from_swapi(self, request):
        """
        Sync planets from external SWAPI API.

        Fetches planet data from SWAPI and creates/updates local planet records.
        Requires SWAPI_PLANETS_URL environment variable to be set.

        Returns:
            dict: Response with number of planets imported or updated
        """
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
