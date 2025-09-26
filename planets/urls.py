from rest_framework.routers import DefaultRouter

from planets.views import ClimateViewSet, PlanetViewSet, TerrainViewSet

router = DefaultRouter()
router.register(r"planets", PlanetViewSet, basename="planet")
router.register(r"climates", ClimateViewSet, basename="climate")
router.register(r"terrains", TerrainViewSet, basename="terrain")

urlpatterns = router.urls
