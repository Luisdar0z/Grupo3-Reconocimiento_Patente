import * from formValidationApp.models
from django.forms import ModelForm 
from django import forms 

class VehiculoForm(ModelForm): 
	class Meta: 
		model = Vehiculo
		fields = ['nombrePersona', 'patente', 'tipo', 'estacionamiento', 'deptoAsociado', 'estado', 'rut', 'email', 'telefono']

	#Funcion usada para la validacion
	def clean(self):
		super(VehiculoForm, self).clean() #Se obtienen los datos del formulario
		
		#Extrae datos de patente y rut
		patente = self.cleaned_data.get('patente')
		rut = self.cleaned_data.get('rut')

		# Condiciones de error
		if len(rut) < 8:
			self._errors['rut'] = self.error_class([
				'Formato de RUT incorrecto.'])
		if len(rut) > 9:
			self._errors['rut'] = self.error_class([
				'Formato de RUT incorrecto.'])
		if ('.' in rut) or ('-' in rut):
			self._errors['rut'] = self.error_class([
				'Ingrese RUT sin puntos ni guión.'])
		if (len(patente) < 7) or (len(patente) > 7):
			self._errors['rut'] = self.error_class([
				'Patente debe tener 7 dígitos exactos incluyendo el guión.'])
		
		# Retorna los errores si existen
		return self.cleaned_data
