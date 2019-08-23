from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Vehiculo, VehiculoFactory
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.
class HomePageView(TemplateView):
	def get(self, request, **kwargs):
		return render(request, 'index.html', context=None)

class HomeVehiculosView(LoginRequiredMixin, TemplateView):
	def get(self, request, **kwargs):
		return render(request, 'vehiculos.html', {'vehiculos': Vehiculo.vehiculos.all()})

class DetalleVehiculoView(LoginRequiredMixin, TemplateView):
	def get(self, request, **kwargs):
		rut = kwargs["rut"]
		return render(request, 'detalleVehiculo.html', {'vehiculo': Vehiculo.vehiculos.get(rut=rut)})
		
class VehiculoCreate(CreateView):
	model = Vehiculo
	template_name = './vehiculo_form.html'
	fields = '__all__'
	
class VehiculoUpdate(UpdateView):
	model = Vehiculo
	template_name = './vehiculo_update.html'
	fields = ['nombrePersona', 'patente', 'estacionamiento', 'deptoAsociado', 'estado', 'rut', 'email', 'telefono']
	
class VehiculoDelete(DeleteView):
	model = Vehiculo
	template_name = './vehiculo_confirm_delete.html'
	success_url = reverse_lazy('patentes')
	