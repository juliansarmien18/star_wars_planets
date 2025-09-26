from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from planets.models import Climate, Planet, Terrain


class PlanetViewSetTestCase(APITestCase):
    """Tests para PlanetViewSet - CRUD básico"""

    def setUp(self):
        """Configuración inicial para cada test"""
        # Crear usuario y autenticarlo
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)

        self.planet_data = {
            "name": "Tatooine",
            "population": "200000",
            "climates": ["arid", "hot"],
            "terrains": ["desert", "canyons"],
        }
        self.planet = Planet.objects.create(name="Test Planet", population="100000")

    def test_create_planet(self):
        """Test crear planeta"""
        url = reverse("planet-list")
        response = self.client.post(url, self.planet_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Planet.objects.count(), 2)
        self.assertEqual(Planet.objects.last().name, "Tatooine")

    def test_list_planets(self):
        """Test listar planetas"""
        url = reverse("planet-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_planet(self):
        """Test obtener planeta específico"""
        url = reverse("planet-detail", kwargs={"pk": self.planet.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Planet")

    def test_update_planet(self):
        """Test actualizar planeta"""
        url = reverse("planet-detail", kwargs={"pk": self.planet.pk})
        update_data = {"name": "Updated Planet", "population": "300000"}
        response = self.client.put(url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.planet.refresh_from_db()
        self.assertEqual(self.planet.name, "Updated Planet")

    def test_partial_update_planet(self):
        """Test actualización parcial de planeta"""
        url = reverse("planet-detail", kwargs={"pk": self.planet.pk})
        update_data = {"population": "500000"}
        response = self.client.patch(url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.planet.refresh_from_db()
        self.assertEqual(self.planet.population, 500000)

    def test_delete_planet(self):
        """Test eliminar planeta"""
        url = reverse("planet-detail", kwargs={"pk": self.planet.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Planet.objects.count(), 0)

    def test_search_planets(self):
        """Test búsqueda de planetas"""
        url = reverse("planet-list")
        response = self.client.get(url, {"search": "Test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)


class ClimateViewSetTestCase(APITestCase):
    """Tests para ClimateViewSet - CRUD básico"""

    def setUp(self):
        """Configuración inicial para cada test"""
        # Crear usuario y autenticarlo
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)

        self.climate_data = {"name": "arid"}
        self.climate = Climate.objects.create(name="hot")

    def test_create_climate(self):
        """Test crear clima"""
        url = reverse("climate-list")
        response = self.client.post(url, self.climate_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Climate.objects.count(), 2)
        self.assertEqual(Climate.objects.last().name, "arid")

    def test_list_climates(self):
        """Test listar climas"""
        url = reverse("climate-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_climate(self):
        """Test obtener clima específico"""
        url = reverse("climate-detail", kwargs={"pk": self.climate.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "hot")

    def test_update_climate(self):
        """Test actualizar clima"""
        url = reverse("climate-detail", kwargs={"pk": self.climate.pk})
        update_data = {"name": "cold"}
        response = self.client.put(url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.climate.refresh_from_db()
        self.assertEqual(self.climate.name, "cold")

    def test_partial_update_climate(self):
        """Test actualización parcial de clima"""
        url = reverse("climate-detail", kwargs={"pk": self.climate.pk})
        update_data = {"name": "windy"}
        response = self.client.patch(url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.climate.refresh_from_db()
        self.assertEqual(self.climate.name, "windy")

    def test_delete_climate(self):
        """Test eliminar clima"""
        url = reverse("climate-detail", kwargs={"pk": self.climate.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Climate.objects.count(), 0)

    def test_search_climates(self):
        """Test búsqueda de climas"""
        url = reverse("climate-list")
        response = self.client.get(url, {"search": "hot"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)


class TerrainViewSetTestCase(APITestCase):
    """Tests para TerrainViewSet - CRUD básico"""

    def setUp(self):
        """Configuración inicial para cada test"""
        # Crear usuario y autenticarlo
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)

        self.terrain_data = {"name": "desert"}
        self.terrain = Terrain.objects.create(name="mountain")

    def test_create_terrain(self):
        """Test crear terreno"""
        url = reverse("terrain-list")
        response = self.client.post(url, self.terrain_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Terrain.objects.count(), 2)
        self.assertEqual(Terrain.objects.last().name, "desert")

    def test_list_terrains(self):
        """Test listar terrenos"""
        url = reverse("terrain-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_terrain(self):
        """Test obtener terreno específico"""
        url = reverse("terrain-detail", kwargs={"pk": self.terrain.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "mountain")

    def test_update_terrain(self):
        """Test actualizar terreno"""
        url = reverse("terrain-detail", kwargs={"pk": self.terrain.pk})
        update_data = {"name": "plateau"}
        response = self.client.put(url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.terrain.refresh_from_db()
        self.assertEqual(self.terrain.name, "plateau")

    def test_partial_update_terrain(self):
        """Test actualización parcial de terreno"""
        url = reverse("terrain-detail", kwargs={"pk": self.terrain.pk})
        update_data = {"name": "canyon"}
        response = self.client.patch(url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.terrain.refresh_from_db()
        self.assertEqual(self.terrain.name, "canyon")

    def test_delete_terrain(self):
        """Test eliminar terreno"""
        url = reverse("terrain-detail", kwargs={"pk": self.terrain.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Terrain.objects.count(), 0)

    def test_search_terrains(self):
        """Test búsqueda de terrenos"""
        url = reverse("terrain-list")
        response = self.client.get(url, {"search": "mountain"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
