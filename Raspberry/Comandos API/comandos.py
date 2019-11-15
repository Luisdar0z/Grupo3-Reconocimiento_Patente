import requests
import json

#Agregar Datos
#Agregar(idvehiculo, hora, fecha, entrada, salida, visto, registrado, patente)
def Agregar(_id, _hora, _fecha, _entrada, _salida, _visto, _registrado):
	#print("imprimiendo desde comandos: ")
	#print(_id)
	#print(_hora)
	#print(_fecha)
	#print(_visto)
	
	url = "http://localhost:8000/apiregistro/"

	_headers = {
		"Content-Type": "application/json",
		"Authorization": "Token 01c8574a530b397e9b20108271b82d3bf8c18906"
	}

	data = {
		"vehiculo": _id,
		"hora": _hora,
		"fecha": _fecha,
		"entrada": _entrada,
		"salida": _salida,
		"visto": _visto,
		"registrado": _registrado
    }

	data_convert = json.dumps(data)
	print(data_convert)

	response = requests.post(url, data=data_convert, headers=_headers)
	print(response.text)
