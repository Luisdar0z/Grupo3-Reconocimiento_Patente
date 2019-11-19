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

# Funcion para verificar si la una lista o matriz esta vacia
def is_empty(data_estructure):
	if data_estructure:
		return False
	else:
		return True

# Funcion para realizar queries de seleccion en la base de datos
def QueryBD(query):
	conn = sqlite3.connect("../proyecto/db.sqlite3")
	c = conn.cursor()
	c.execute(query)
	templist=list(c.fetchall())
	return templist

# Funcion para construir los arreglos con tiempos promedio para analitica
def Construccion_arreglo_tiempos(matriz):
	arreglo_tiempos = []
	
	i = 0
	entrada = 0
	salida = 0
	flag_entrada = 0
	flag_salida = 0
	
	while i < len(matriz):
		if (matriz[i][1] == 1):
			aux = (matriz[i][0]).split(":")
			entrada = int(aux[0])*60 + int(aux[1])
			flag_entrada = 1
		elif (matriz[i][2] == 1):
			aux = (matriz[i][0]).split(":")
			salida = int(aux[0])*60 + int(aux[1])
			flag_salida = 1
		if (flag_entrada == 1 and flag_salida == 1):
			res = salida - entrada
			arreglo_tiempos.append(res)
			flag_entrada = 0
			flag_salida = 0
		i = i + 1
	
	return arreglo_tiempos



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

class ReportesForm(PermissionRequiredInGroupMixin, LoginRequiredMixin, TemplateView):
	permission_required = 'puede_ver_registros'
	model = RegistroVehiculos
	template_name = './registrovehiculos_form.html'
	fields = ['fecha']

class ReportesView(PermissionRequiredInGroupMixin, LoginRequiredMixin, TemplateView):
	permission_required = 'puede_ver_registros'
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

class AnaliticaView(PermissionRequiredInGroupMixin, LoginRequiredMixin, TemplateView):
	permission_required = 'puede_ver_analiticas'
	template_name = './analytics.html'
	
# Funcion que construye el set de datos para la analitica de tiempo promedio de estancia de visita y servicios
def AnaliticaDatos_Tiempo(request, *args, **kwargs):
	visitas_tiempo = []
	servicios_tiempo = []
	tiempo_promedio = []
	resultado_tiempo = 0

	queryVisitas = "SELECT api_registrovehiculos.hora, api_registrovehiculos.entrada, api_registrovehiculos.salida FROM (api_registrovehiculos INNER JOIN patentes_vehiculo ON api_registrovehiculos.vehiculo = patentes_vehiculo.id) WHERE patentes_vehiculo.tipo = 'Visita';"
	visitas = QueryBD(queryVisitas)
	
	# Si no existen datos, se agrega un cero
	if is_empty(visitas) is True:
		servicios_tiempo.append(0)

	queryServicios = "SELECT api_registrovehiculos.hora, api_registrovehiculos.entrada, api_registrovehiculos.salida FROM (api_registrovehiculos INNER JOIN patentes_vehiculo ON api_registrovehiculos.vehiculo = patentes_vehiculo.id) WHERE patentes_vehiculo.tipo = 'Servicios';"
	servicios = QueryBD(queryServicios)
	
	# Si no existen datos, se agrega un cero
	if is_empty(servicios) is True:
		servicios_tiempo.append(0)

	# Construccion de arreglo de con los tiempos de visitas
	visitas_tiempo = Construccion_arreglo_tiempos(visitas)

	# Si no existen datos para calcular, se agrega un cero
	if is_empty(visitas_tiempo) is True:
		visitas_tiempo.append(0)

	# Construccion de arreglo de con los tiempos de vehiculos de servicios
	servicios_tiempo = Construccion_arreglo_tiempos(servicios)
	
	# Si no existen datos para calcular, se agrega un cero
	if is_empty(servicios_tiempo) is True:
		servicios_tiempo.append(0)

	# Calculo de los tiempos promedio
	resultado_tiempo = mean(visitas_tiempo)
	tiempo_promedio.append(resultado_tiempo)
	resultado_tiempo = mean(servicios_tiempo)
	tiempo_promedio.append(resultado_tiempo)

	labels = ["Visitas", "Servicios"]

	data = {
		"labels": labels,
		"tiempo": tiempo_promedio,
	}
	return JsonResponse(data)

# Funcion que construye el set de datos para la analitica de cantidad de visitas y servicios en el dia
def AnaliticaDatos_Cantidad_al_Dia(request, *args, **kwargs):
	fecha = time.strftime("%Y-%m-%d")
	fecha = '2019-09-20'
	
	queryVisitas = "SELECT COUNT(*) FROM (api_registrovehiculos INNER JOIN patentes_vehiculo ON api_registrovehiculos.vehiculo = patentes_vehiculo.id) WHERE patentes_vehiculo.tipo = 'Visita' AND api_registrovehiculos.fecha = '" + fecha + "';"
	visitas = QueryBD(queryVisitas)

	queryServicios = "SELECT COUNT(*) FROM (api_registrovehiculos INNER JOIN patentes_vehiculo ON api_registrovehiculos.vehiculo = patentes_vehiculo.id) WHERE patentes_vehiculo.tipo = 'Servicios' AND api_registrovehiculos.fecha = '" + fecha + "';"
	servicios = QueryBD(queryServicios)

	labels = ["Visitas", "Servicios"]

	data = {
		"labels": labels,
		"cantidad": [visitas[0][0], servicios[0][0]],
	}
	return JsonResponse(data)

# Funcion que construye el set de datos para la analitica de cantidad de ingreso de visitas al mes por horario
def AnaliticaDatos_Horarios(request, *args, **kwargs):
	fecha = time.strftime("%Y-%m-%d")
	auxFecha = fecha.split("-")
	
	fecha_inicio = auxFecha[0] + "-" + auxFecha[1] + "-01"
	fecha_termino = auxFecha[0] + "-" + auxFecha[1] + "-30"
	fecha_inicio = '2019-09-01'
	fecha_termino = '2019-09-30'
	
	labels = []
	cantidad = []
	
	cantidad_por_horarios = [["0:00", 0], ["1:00", 0], ["2:00", 0], ["3:00", 0],
							["4:00", 0], ["5:00", 0], ["6:00", 0], ["7:00", 0],
							["8:00", 0], ["9:00", 0], ["10:00", 0], ["11:00", 0],
							["12:00", 0], ["13:00", 0], ["14:00", 0], ["15:00", 0],
							["16:00", 0], ["17:00", 0], ["18:00", 0], ["19:00", 0],
							["20:00", 0], ["21:00", 0], ["22:00", 0], ["23:00", 0]]
	
	queryVisitas = "SELECT * FROM (api_registrovehiculos INNER JOIN patentes_vehiculo ON api_registrovehiculos.vehiculo = patentes_vehiculo.id) WHERE patentes_vehiculo.tipo = 'Visita' AND api_registrovehiculos.entrada = 1 AND api_registrovehiculos.fecha > '" + fecha_inicio + "' AND api_registrovehiculos.fecha < '" + fecha_termino + "';"
	visitas = QueryBD(queryVisitas)
	
	# Realiza los conteos para cada horario
	i = 0
	while i < len(visitas):
		aux = (visitas[i][1]).split(":")
		aux = str(aux[0] + ":00")
		j = 0
		while j < len(cantidad_por_horarios):
			if (aux == cantidad_por_horarios[j][0]):
				cont = cantidad_por_horarios[j][1] + 1
				cantidad_por_horarios[j][1] = cont
			j = j + 1
		i = i + 1

	# Ordena resultados de las tuplas en orden descendente
	resultado = sorted(cantidad_por_horarios, key=lambda x: x[1], reverse=True)
	
	i = 0
	while i < len(resultado):
		labels.append(resultado[i][0])
		cantidad.append(resultado[i][1])
		i = i + 1

	data = {
		"labels": labels,
		"cantidad": cantidad,
	}
	return JsonResponse(data)
