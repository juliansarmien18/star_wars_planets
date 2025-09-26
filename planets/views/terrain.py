from django.db import transaction
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from core.utils.pagination import PlanetPagination
from planets.models import Terrain
from planets.serializers import TerrainSerializer


class TerrainViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar CRUD de Terrain
    """

    queryset = Terrain.objects.all().order_by("name")
    serializer_class = TerrainSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PlanetPagination
    filter_backends = [SearchFilter]
    search_fields = ["name"]

    @transaction.atomic
    def perform_create(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            raise Exception(f"Error creating terrain: {str(e)}")

    @transaction.atomic
    def perform_update(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            raise Exception(f"Error updating terrain: {str(e)}")

    @transaction.atomic
    def perform_destroy(self, instance):
        try:
            instance.delete()
        except Exception as e:
            raise Exception(f"Error deleting terrain: {str(e)}")
