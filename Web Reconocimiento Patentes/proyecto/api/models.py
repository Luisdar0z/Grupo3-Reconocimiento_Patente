from django.db import models
from patentes.models import Vehiculo

class RegistroVehiculos(models.Model):
	vehiculo = models.CharField(max_length=7)
	hora = models.CharField(max_length=5)
	fecha = models.DateField(null=True)
	entrada = models.BooleanField(default=False)
	salida = models.BooleanField(default=False)
	visto = models.BooleanField(default=False)
	registrado = models.BooleanField(default=False)
	objects = models.Manager()

	def __str__(self):
		return "{}".format(self.vehiculo)