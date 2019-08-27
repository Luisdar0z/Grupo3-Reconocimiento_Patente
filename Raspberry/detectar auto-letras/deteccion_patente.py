"""Detects text in the file."""
from google.cloud import vision
client = vision.ImageAnnotatorClient()

patente = "" #obtendra la patente del vehiculo

def Espacio(_text):
    global patente
    cont = 0 #obtiene cantidad de espacios
    for i in range(len(_text)):
        if _text[i] == ' ':
            cont += 1
    if cont == 2:
        patente = _text

def Cadenas(split_word):
    for i in range(len(split_word)):
        if len(split_word[i]) == 8:
            Espacio(split_word[i])



def detect_text(path):
    with open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    for text in texts:
        texto = text.description
        words = texto.split('\n', 15) #(caracter para split, cantidad maxima de split)
        Cadenas(words)
        #print('\n"{}"'.format(text.description))
        #print(text.description)
        #Limpieza(text.description)
               
    
    print(patente)
detect_text('ej2-0014.jpg')