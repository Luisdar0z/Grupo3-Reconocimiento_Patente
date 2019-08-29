import sqlite3

patente_rec ="\"DTRC-78\""

def Recon(text_):
	conn = sqlite3.connect("db.sqlite3")
	c = conn.cursor()
	myquery = ("SELECT nombrePersona, telefono, patente FROM patentes_vehiculo WHERE patente =" + text_)
	c.execute(myquery)
	templist=list(c.fetchall())
	print (templist[0][0])

Recon(patente_rec)
