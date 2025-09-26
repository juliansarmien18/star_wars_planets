from django.db import transaction
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from core.utils.pagination import PlanetPagination
from planets.models import Climate
from planets.serializers import ClimateSerializer


class ClimateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing climates.

    Provides CRUD operations for climates including:
    - List all climates with pagination and search
    - Retrieve specific climate details
    - Create new climates
    - Update existing climates
    - Delete climates

    Search functionality allows filtering by climate name.
    """

    queryset = Climate.objects.all().order_by("name")
    serializer_class = ClimateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PlanetPagination
    filter_backends = [SearchFilter]
    search_fields = ["name"]

    @transaction.atomic
    def perform_create(self, serializer):
        """Create a new climate with atomic transaction."""
        try:
            serializer.save()
        except Exception as e:
            raise Exception(f"Error creating climate: {str(e)}")

    @transaction.atomic
    def perform_update(self, serializer):
        """Update an existing climate with atomic transaction."""
        try:
            serializer.save()
        except Exception as e:
            raise Exception(f"Error updating climate: {str(e)}")

    @transaction.atomic
    def perform_destroy(self, instance):
        """Delete a climate with atomic transaction."""
        try:
            instance.delete()
        except Exception as e:
            raise Exception(f"Error deleting climate: {str(e)}")
