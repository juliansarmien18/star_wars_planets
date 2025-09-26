from rest_framework.routers import DefaultRouter

from planets.views import PlanetViewSet

router = DefaultRouter()
router.register(r"planets", PlanetViewSet, basename="planet")

urlpatterns = router.urls
