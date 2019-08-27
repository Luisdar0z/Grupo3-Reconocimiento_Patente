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
	
class VehiculoSearch(TemplateView):
	model = Vehiculo
	template_name = './vehiculo_search.html'
	fields = ['nombrePersona', 'patente', 'estacionamiento', 'deptoAsociado', 'estado', 'rut', 'email', 'telefono']
	
class VehiculoSearchView(LoginRequiredMixin, TemplateView):
	def post(self, request, **kwargs):
		nombrePersona=''
		patente=''
		estacionamiento=''
		deptoAsociado=''
		rut=''
		if "nombrePersona" in request.POST.keys():
			nombrePersona = request.POST["nombrePersona"]
		if "patente" in request.POST.keys():
			patente = request.POST["patente"]
		if "estacionamiento" in request.POST.keys():
			estacionamiento = request.POST["estacionamiento"]
		if "deptoAsociado" in request.POST.keys():
			deptoAsociado = request.POST["deptoAsociado"]
		if "rut" in request.POST.keys():
			rut = request.POST["rut"]
		
		vehiculosResultados = []
		
		if (nombrePersona != ''):
			resultado = Vehiculo.vehiculos.get(nombrePersona=nombrePersona)
			vehiculosResultados.append(resultado)
		elif (patente != ''):
			resultado = Vehiculo.vehiculos.get(patente=patente)
			vehiculosResultados.append(resultado)
		elif (estacionamiento != ''):
			resultado = Vehiculo.vehiculos.get(estacionamiento=estacionamiento)
			vehiculosResultados.append(resultado)
		elif (deptoAsociado != ''):
			resultado = Vehiculo.vehiculos.get(deptoAsociado=deptoAsociado)
			vehiculosResultados.append(resultado)
		elif (rut != ''):
			print(Vehiculo.vehiculos.get(rut=rut))
			resultado = Vehiculo.vehiculos.get(rut=rut)
			vehiculosResultados.append(resultado)
		return render(request, 'vehiculos_results.html', {'vehiculos': vehiculosResultados})