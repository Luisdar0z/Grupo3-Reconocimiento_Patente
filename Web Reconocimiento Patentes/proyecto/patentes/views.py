from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Vehiculo, VehiculoFactory
from api.models import RegistroVehiculos
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

import sqlite3


# Funcion para realizar queries de seleccion en la base de datos
def QueryBD(query):
	conn = sqlite3.connect("../proyecto/db.sqlite3")
	c = conn.cursor()
	c.execute(query)
	templist=list(c.fetchall())
	return templist[0][0]



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
	fields = ['nombrePersona', 'patente', 'tipo', 'estacionamiento', 'deptoAsociado', 'estado', 'rut', 'email', 'telefono']
	
class VehiculoDelete(DeleteView):
	model = Vehiculo
	template_name = './vehiculo_confirm_delete.html'
	success_url = reverse_lazy('patentes')
	
class VehiculoSearch(TemplateView):
	model = Vehiculo
	template_name = './vehiculo_search.html'
	fields = ['nombrePersona', 'patente', 'tipo', 'estacionamiento', 'deptoAsociado', 'estado', 'rut', 'email', 'telefono']
	
class VehiculoSearchView(LoginRequiredMixin, TemplateView):
	def post(self, request, **kwargs):
		nombrePersona=''
		patente=''
		tipo=''
		estacionamiento=''
		deptoAsociado=''
		rut=''
		
		if "nombrePersona" in request.POST.keys():
			nombrePersona = request.POST["nombrePersona"]
		if "patente" in request.POST.keys():
			patente = request.POST["patente"]
		if "tipo" in request.POST.keys():
			tipo = request.POST["tipo"]
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
		elif (tipo != ''):
			_vehiculos = Vehiculo.vehiculos.all()
			for i in _vehiculos:
				if (i.tipo==tipo):
					vehiculosResultados.append(i)
		elif (estacionamiento != ''):
			resultado = Vehiculo.vehiculos.get(estacionamiento=estacionamiento)
			vehiculosResultados.append(resultado)
		elif (deptoAsociado != ''):
			resultado = Vehiculo.vehiculos.get(deptoAsociado=deptoAsociado)
			vehiculosResultados.append(resultado)
		elif (rut != ''):
			resultado = Vehiculo.vehiculos.get(rut=rut)
			vehiculosResultados.append(resultado)
		
		return render(request, 'vehiculos_results.html', {'vehiculos': vehiculosResultados})
	
class VehiculoReconocimiento(LoginRequiredMixin, TemplateView):
	model = Vehiculo
	template_name = './vehiculo_reconocimiento.html'
	
	def get(self, request, **kwargs):
		query = 'SELECT patentes_vehiculo.id FROM (patentes_vehiculo inner join api_registrovehiculos on patentes_vehiculo.id = api_registrovehiculos.vehiculo) ORDER BY api_registrovehiculos.id DESC LIMIT 1'		
		vehiculo = Vehiculo.vehiculos.raw(query)
		
		queryID = "SELECT * FROM api_registrovehiculos ORDER BY api_registrovehiculos.id DESC LIMIT 1;"
		registro_vehiculo = RegistroVehiculos.objects.raw(queryID)
		id = str(QueryBD(queryID))
			
		if request.GET.get('visto', False):
			RegistroVehiculos.objects.filter(pk=id).update(visto='1')
		
		return render(request, 'vehiculo_reconocimiento.html', {'vehiculos': vehiculo, 'registro_vehiculos': registro_vehiculo})
	
class ReportesForm(TemplateView):
	model = RegistroVehiculos
	template_name = './registrovehiculos_form.html'
	fields = ['fecha']
	
class ReportesView(LoginRequiredMixin, TemplateView):
	def post(self, request, **kwargs):
		vehiculosResultados = []
		
		if "fechaInicio" in request.POST.keys():
			fechaInicio = request.POST["fechaInicio"]
		if "fechaTermino" in request.POST.keys():
			fechaTermino = request.POST["fechaTermino"]
		
		query = "SELECT * FROM api_registrovehiculos WHERE fecha >= '" + fechaInicio + "' and fecha <= '" + fechaTermino + "'"
		resultados = RegistroVehiculos.objects.raw(query)
		
		for resultado in resultados:
			vehiculo = Vehiculo.vehiculos.get(id=resultado.vehiculo)
			vehiculosResultados.append(vehiculo)
		
		return render(request, 'registrovehiculos_results.html', {'registro_vehiculos': resultados, 'vehiculos': vehiculosResultados})
