#cuenta espacio de cadena para poder obtener la patente
def Espacio(cadena):
    global patente
    cont = 0 #obtiene cantidad de espacios
    if (cadena[2] == ' ') and (cadena[5] == ' '):
        patente = cadena

def Cadenas(split_word):
    for i in range(len(split_word)):
        if len(split_word[i]) == 8:
            Espacio(split_word[i])


word = "VOYAGE\nMarubeni\nLD KY 95\nCHILE\n" #caso ejemplo
words = word.split('\n', 15) #(caracter para split, cantidad maxima de split)
patente = "" #obtendra la patente del vehiculo

Cadenas(words)

print(patente)
