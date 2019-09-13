import sqlite3

patente_rec ="\"ASDF-34\""

def Recon(text_):
	conn = sqlite3.connect("db.sqlite3")
	c = conn.cursor()
	query = ("SELECT api_registrovehiculos.id FROM (api_registrovehiculos inner join patentes_vehiculo on api_registrovehiculos.vehiculo = patentes_vehiculo.id) WHERE patentes_vehiculo.patente = "+ text_)
	c.execute(query)
	templist=list(c.fetchall())
	print (templist[0][0])

Recon(patente_rec)
