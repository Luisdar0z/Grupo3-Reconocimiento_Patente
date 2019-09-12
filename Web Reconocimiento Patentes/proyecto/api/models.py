from django.db import models

class RegistroVehiculos(models.Model):
	vehiculo = models.IntegerField()
	hora = models.CharField(max_length=5)
	day = models.IntegerField()
	month = models.IntegerField()
	year = models.IntegerField()
		
	def __str__(self):
		return "{}".format(self.vehiculo)