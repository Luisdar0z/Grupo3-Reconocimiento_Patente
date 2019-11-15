import time
import sqlite3
from comandos import *

# Funcion para verificar si la una lista o matriz esta vacia
def is_empty(data_estructure):
	if data_estructure:
		return False
	else:
		return True

# Funcion para obtener el ID del vehiculo reconocido
def Recon(text_):
	conn = sqlite3.connect("../../Web Reconocimiento Patentes/proyecto/db.sqlite3")
	c = conn.cursor()
	query = ("SELECT id FROM patentes_vehiculo WHERE patente = " + "\"" + text_ + "\"")
	c.execute(query)
	templist = list(c.fetchall())
	
	#Si encontro vehiculo registrado
	if is_empty(templist) is False:
		query2 = ("SELECT tipo FROM patentes_vehiculo WHERE patente = " + "\"" + text_ + "\"")
		c.execute(query2)
		templist2 = list(c.fetchall())
		if (templist2[0][0] == 'Residente') or (templist2[0][0] == 'Visita') or (templist2[0][0] == 'Servicios'):
			return templist[0][0]
	#Si no encontro vehiculo registrado
	else:
		return -1

# Funcion para verificar si el vehiculo ya habia entrado y, por ende, definir que esta saliendo
def Entro(_id):
	conn = sqlite3.connect("../../Web Reconocimiento Patentes/proyecto/db.sqlite3")
	c = conn.cursor()
	query = "SELECT entrada FROM api_registrovehiculos WHERE vehiculo = "+ str(_id) +" ORDER BY api_registrovehiculos.id DESC LIMIT 1;"
	c.execute(query)
	templist = list(c.fetchall())
	
	if is_empty(templist) is False:
		#Si el vehiculo ya habia ingresado
		if (templist[0][0] == 1):
			return 1
		#Si no ha ingresado
		else:
			return 0
	else:
		return 0

# Funcion para postar un nuevo registro en la API
def Post_Vehiculo_Reconocido(_id, _registrado):
	hora = time.strftime("%H:%M")
	fecha = time.strftime("%Y-%m-%d")
	
	#Agregar(idvehiculo, hora, fecha, entrada, salida, visto, registrado)
	if (_registrado == 1):
		if (Entro(_id) == 1):
			Agregar(_id, hora, fecha, 0, 1, 0, _registrado)
		else:
			Agregar(_id, hora, fecha, 1, 0, 0, _registrado)
	else:
		Agregar(_id, hora, fecha, 1, 0, 0, _registrado)

patente_rec = "ASDF-35"
id = Recon(patente_rec)
#print(id)

if id > 0:
	print("Vehiculo Registrado")
	Post_Vehiculo_Reconocido(id, 1)
else:
	print("Vehiculo no conocido")
	Post_Vehiculo_Reconocido(patente_rec, 0)
