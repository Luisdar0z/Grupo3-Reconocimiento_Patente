from django.test import TestCase

from .models import RegistroVehiculos
from rest_framework.test import APIClient
from rest_framework import status
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User

class RegistroVehiculosTestCase(TestCase):
	"""Esta clase define la testsuite para el Vehiculo"""

	def setUp(self):
		"""Definicion de variables generales"""		
		self.vehiculo = 4
		self.hora = "17:02"
		self.fecha = "2019/09/18"
		self.visto = "false"
		self.registrovehiculos = RegistroVehiculos(
			vehiculo=self.vehiculo,
			hora=self.hora,
			fecha=self.fecha
			visto=self.visto
		)
		
	def test_creacion_de_vehiculo(self):
		"""Test de creación de un vehiculo"""
		old_count = RegistroVehiculos.objects.count()
		self.registrovehiculos.save()
		new_count = RegistroVehiculos.objects.count()
		self.assertNotEqual(old_count, new_count)

class ViewTestCase(TestCase):
	"""Esta clase define la testsuite para la API REST"""

	def setUp(self):
		"""Definicion de variables generales"""
		self.user=User.objects.create_superuser('servidor', 'api@servidor.com', "Secret.123")
		c = Client()
		response = c.post('/api/login', {'username':'servidor', 'password':'Secret.123'})
		self.token = response.json()["token"]
		self.client = APIClient()
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
		
		registro_vehiculos_data = {'vehiculo':4,'hora':'17:02','fecha':'2019/09/18', 'visto': 'false'}
		self.response_setup = self.client.post(
			reverse('create'),
			registro_vehiculos_data,
			format='json')

	def test_api_creacion_de_recursos(self):
		"""Test creación de vehiculo a través de la API"""
		self.assertEqual(self.response_setup.status_code, status.HTTP_201_CREATED)

	def test_api_obtener_vehiculo(self):
		"""Test de obtención de vehiculo a través de la API."""
		registro_vehiculos = RegistroVehiculos.objects.get()
		response = self.client.get(
			reverse('details',
			kwargs={'pk': registro_vehiculos.id}), format="json")

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertContains(response, registro_vehiculos)
		
	def test_api_actualizar_vehiculo(self):
		"""Test de actualización de vehiculo a través de la API."""
		registro_vehiculos = RegistroVehiculos.objects.get()
		actualizacion_vehiculo = {'visto': 'true'}
		res = self.client.patch(
			reverse('details', kwargs={'pk': registro_vehiculos.id}),
			actualizacion_vehiculo, format='json'
		)
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		
	def test_api_borrar_vehiculo(self):
		"""Test borrado de vehiculo a través de la API"""
		registro_vehiculos = RegistroVehiculos.objects.get()
		response = self.client.delete(
			reverse('details', kwargs={'pk': registro_vehiculos.id}),
			format = 'json',
			follow = True
		)
		self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
