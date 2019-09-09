from rest_framework import serializers
from .models import RegistroVehiculos


class RegistroVehiculosSerializer(serializers.ModelSerializer):
	"""Serializador para mapear un vehiculo a formato JSON"""
	
	class Meta:
		"""Meta clase para el mapeo de atributos"""
		model = RegistroVehiculos
		fields = (	'id',
					'vehiculo',
				  	'hora',
					'day',
					'month',
					'year'
				 )
		read_only_fields = ()