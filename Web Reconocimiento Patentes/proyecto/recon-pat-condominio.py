import sqlite3

patente_rec ="\"ASDF-34\""

def Recon(text_):
	conn = sqlite3.connect("db.sqlite3")
	c = conn.cursor()
	query = ("SELECT id FROM patentes_vehiculo WHERE patentes_vehiculo.patente = "+ text_)
	c.execute(query)
	templist=list(c.fetchall())
	print (templist[0][0])

Recon(patente_rec)
