import time
import sqlite3
from comandos import *

def Recon(text_):
    conn = sqlite3.connect("/home/francisco/Documentos/Grupo3-Reconocimiento_Patente/Web Reconocimiento Patentes/proyecto/db.sqlite3")
    c = conn.cursor()
    query = ("SELECT id FROM patentes_vehiculo WHERE patentes_vehiculo.patente = "+ text_)
    c.execute(query)
    templist=list(c.fetchall())
    #print (templist[0][0])
    return templist[0][0]

patente_rec ="\"ASDF-34\""
id = Recon(patente_rec)
#print(id)


hora = time.strftime("%H:%M")
#print(hora)
dia = time.strftime("%d")
mes = time.strftime("%m")
anio = time.strftime("%y")
#print(dia)
#print(mes)
#print(anio)

Agregar(id, hora, dia, mes, anio)
