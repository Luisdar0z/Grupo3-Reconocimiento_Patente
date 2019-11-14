from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Vehiculo, VehiculoFactory
from api.models import RegistroVehiculos
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import View

from django.http import JsonResponse

import time
import sqlite3
from statistics import mean



# Verificacion de permisos
class PermissionRequiredInGroupMixin(PermissionRequiredMixin):
    def has_permission(self):
        usuario = self.request.user
        permisos = self.get_permission_required()
        privilegios = []
        
        for g in usuario.groups.all():
            for p in g.permissions.all():
                privilegios.append(p.codename)
        for r in permisos:
            if r not in privilegios:
                return False
        return True

# Funcion para realizar queries de seleccion en la base de datos
def QueryBD(query):
	conn = sqlite3.connect("../proyecto/db.sqlite3")
	c = conn.cursor()
	c.execute(query)
	templist=list(c.fetchall())
	return templist




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

class VehiculoSearch(PermissionRequiredInGroupMixin, TemplateView):
	permission_required = 'puede_buscar_vehiculos'
	model = Vehiculo
	template_name = './vehiculo_search.html'
	fields = ['nombrePersona', 'patente', 'tipo', 'estacionamiento', 'deptoAsociado', 'estado', 'rut', 'email', 'telefono']

class VehiculoSearchView(PermissionRequiredInGroupMixin, LoginRequiredMixin, TemplateView):
	permission_required = 'puede_buscar_vehiculos'
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
		vehiculo = []
		
		queryID = "SELECT * FROM api_registrovehiculos ORDER BY api_registrovehiculos.id DESC LIMIT 1;"
		registro_vehiculo = RegistroVehiculos.objects.raw(queryID)
		registro = QueryBD(queryID)
		
		# Si esta registrado
		if (registro[0][4] != 0):
			query = ("SELECT * FROM patentes_vehiculo WHERE id = " + "\"" + str(registro[0][7]) + "\"")
			id_vehiculo = QueryBD(query)
			
			if request.GET.get('visto', False):
				RegistroVehiculos.objects.filter(pk=registro[0][0]).update(visto='1')
				v = Vehiculo.vehiculos.get(id=id_vehiculo[0][0])
				vehiculo.append(v)
		# Si no esta registrado
		else:		
			if request.GET.get('visto', False):
				query = ("SELECT * FROM patentes_vehiculo WHERE patente = " + "\"" + str(registro[0][7]) + "\"")
				id_vehiculo = QueryBD(query)
				RegistroVehiculos.objects.filter(pk=registro[0][0]).update(vehiculo=id_vehiculo[0][0])
				RegistroVehiculos.objects.filter(pk=registro[0][0]).update(visto='1')
				RegistroVehiculos.objects.filter(pk=registro[0][0]).update(registrado='1')
		
		return render(request, 'vehiculo_reconocimiento.html', {'vehiculos': vehiculo, 'registro_vehiculos': registro_vehiculo})

class ReportesForm(PermissionRequiredInGroupMixin, TemplateView):
	permission_required = 'puede_buscar_vehiculos'
	model = RegistroVehiculos
	template_name = './registrovehiculos_form.html'
	fields = ['fecha']

class ReportesView(PermissionRequiredInGroupMixin, LoginRequiredMixin, TemplateView):
	permission_required = 'puede_buscar_vehiculos'
	def post(self, request, **kwargs):
		vehiculosResultados = []
		nombres = []
		fechas = []
		horas = []

		if "fechaInicio" in request.POST.keys():
			fechaInicio = request.POST["fechaInicio"]
		if "fechaTermino" in request.POST.keys():
			fechaTermino = request.POST["fechaTermino"]
		
		query = "SELECT * FROM api_registrovehiculos WHERE fecha >= '" + fechaInicio + "' and fecha <= '" + fechaTermino + "'"
		resultados = RegistroVehiculos.objects.raw(query)

		for r in resultados:
			if (r.entrada == 1):
				vehiculo = Vehiculo.vehiculos.get(id=r.vehiculo)
				vehiculosResultados.append(vehiculo)
				fechas.append(r.fecha)
				horas.append(r.hora)
		
		for v in vehiculosResultados:
			nombres.append(v.nombrePersona)
			
		reporte = list(zip(nombres, fechas, horas))
		
		return render(request, 'registrovehiculos_results.html', {'reporte': reporte})
