import time
import sqlite3
from comandos import *

def is_empty(data_estructure):
    if data_estructure:
        return False
    else:
        return True

def Recon(text_):
    conn = sqlite3.connect("/home/francisco/Documentos/Grupo3-Reconocimiento_Patente/Web Reconocimiento Patentes/proyecto/db.sqlite3")
    c = conn.cursor()
    query = ("SELECT id FROM patentes_vehiculo WHERE patentes_vehiculo.patente = "+ text_)
    c.execute(query)
    templist=list(c.fetchall())
    #tiene datos
    if is_empty(templist) is False:
        query2 = ("SELECT tipo FROM patentes_vehiculo WHERE patentes_vehiculo.patente = "+ text_)
        c.execute(query2)
        templist2 = list(c.fetchall())
        if (templist2[0][0] == 'Residente') or (templist2[0][0] == 'Visita') or (templist2[0][0] == 'Servicios'):
            return templist[0][0]
    #esta vacio
    else:
        return -1


def Conocido(_id):
    hora = time.strftime("%H:%M")
    # print(hora)
    dia = time.strftime("%d")
    mes = time.strftime("%m")
    anio = time.strftime("%y")
    # print(dia)
    # print(mes)
    # print(anio)

    Agregar(id, hora, anio, mes, dia)



patente_rec ="\"ASDF-34\""
id = Recon(patente_rec)
print(id)
if id>0:
    Conocido(id)
else:
    print("Vehiculo no conocido")
