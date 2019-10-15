from django.shortcuts import render
from rest_framework import generics
from .serializers import RegistroVehiculosSerializer
from .models import RegistroVehiculos
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
	HTTP_400_BAD_REQUEST,
	HTTP_404_NOT_FOUND,
	HTTP_200_OK
)
from rest_framework.response import Response



class CreateView(generics.ListCreateAPIView):
	"""Vista que representa el comportamiento de la API REST."""
	#El queryset contiene la colección con todos los vehiculos
	queryset = RegistroVehiculos.objects.all()
	serializer_class = RegistroVehiculosSerializer

	def perform_create(self, serializer):
		"""Almacena los datos recibidos mediante POST como un Curso."""
		serializer.save()

class DetailsView(generics.RetrieveUpdateDestroyAPIView):
	"""Vista que maneja las peticiones GET, PUT y DELETE."""
	queryset = RegistroVehiculos.objects.all()
	serializer_class = RegistroVehiculosSerializer

	
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
	username = request.data.get("username")
	password = request.data.get("password")
	if username is None or password is None:
		return Response({'error': 'Please provide both username and password'},
					   status=HTTP_400_BAD_REQUEST)
	user = authenticate(username=username, password=password)
	if not user:
		return Response({'error': 'Invalid Credentials'},
					   status=HTTP_404_NOT_FOUND)
	token, _ = Token.objects.get_or_create(user=user)
	return Response({'token': token.key},
				   status=HTTP_200_OK)
