from django.db import models

class RegistroVehiculos(models.Model):
	vehiculo = models.PositiveIntegerField()
	hora = models.CharField(max_length=5)
	day = models.PositiveIntegerField()
	month = models.PositiveIntegerField()
	year = models.PositiveIntegerField()
		
	def __str__(self):
		return "{}".format(self.vehiculo)