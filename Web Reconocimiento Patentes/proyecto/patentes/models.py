from django.db import models

# Create your models here.
class Vehiculo(models.Model):
	nombrePersona = models.CharField(max_length=28)
	patente = models.CharField(max_length=7)
	estacionamiento = models.CharField(max_length=10)
	deptoAsociado = models.CharField(max_length=10)
	estado = models.CharField(max_length=10)
	rut = models.CharField(max_length=9)
	email = models.CharField(max_length=28)
	telefono = models.CharField(max_length=12)
	vehiculos = models.Manager()
		
	def __str__(self):
		return "{}".format(self.nombrePersona)
		
class VehiculoFactory:
	def __init__(self):
		self.vehiculos = []
		#self.vehiculos.append(Vehiculo("Juan Perez", "ACBD-12", "A02", "1006", "Activo", "66666666", "asdasd@asd.cl", "555-666-777"))
		#self.vehiculos.append(Vehiculo("Maldito Gabrielito", "FGHI-34", "A03", "1007", "Activo", "77777773", "qqqqqq@asd.cl", "666-777-888"))

	def obtenerVehiculos(self):
		return self.vehiculos

	def getVehiculo(self, rut):
		for vehiculo in self.vehiculos:
			if vehiculo.rut == rut:
				return vehiculo
		return None