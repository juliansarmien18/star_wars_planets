from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

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
