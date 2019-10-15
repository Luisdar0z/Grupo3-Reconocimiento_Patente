from django.db import models

class RegistroVehiculos(models.Model):
	vehiculo = models.PositiveIntegerField()
	hora = models.CharField(max_length=5)
	fecha = models.DateField(null=True)
	visto = models.BooleanField(default=False)
	objects = models.Manager()

	def __str__(self):
		return "{}".format(self.vehiculo)