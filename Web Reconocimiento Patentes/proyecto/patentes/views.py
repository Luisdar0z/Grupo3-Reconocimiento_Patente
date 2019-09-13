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
	
	def myView(request):
		form = myForm(request.POST or None)
		if request.method == 'POST':
			if form.is_valid():
				return HttpResponseRedirect('/gracias/')
		return render_to_response('vehiculo_form.html', {'form': form})
	
class VehiculoUpdate(UpdateView):
	model = Vehiculo
	template_name = './vehiculo_update.html'
	fields = ['nombrePersona', 'patente', 'tipo', 'estacionamiento', 'deptoAsociado', 'estado', 'rut', 'email', 'telefono']
	
	def myView(request):
		form = myForm(request.POST or None)
		if request.method == 'POST':
			if form.is_valid():
				return HttpResponseRedirect('/gracias/')
		return render_to_response('vehiculo_update.html', {'form': form})
	
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
	
#class VehiculoReconocimiento(LoginRequiredMixin, TemplateView):
	#def Reconocimiento(self, request, **kwargs):
		#p=Vehiculo.objects.raw(query)
		#return render(request, 'vehiculo_reconocimiento.html', {'vehiculos': p})