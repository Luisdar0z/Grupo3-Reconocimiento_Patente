"""Detects text in the file."""
from google.cloud import vision
client = vision.ImageAnnotatorClient()

patente = "" #obtendra la patente del vehiculo

def EspacioAuto(_text):
    global patente
    if ((cadena[2] == ' ') or (cadena[2] == '.')) and ((cadena[5] == ' ') or (cadena[5] == '-')):
        patente = _text

def EspacioMoto(_text):
    global patente
    if cadena[3] == ' ' or cadena[3] == '-' or cadena[3] == '.':
        patente = _text

def Cadenas(split_word):
    for i in range(len(split_word)):
        if len(split_word[i]) == 8:
            EspacioAuto(split_word[i])
        elif len(split_word[i]) == 6:
            EspacioMoto(split_word[i])


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
    print(patente)


detect_text('ej2-0014.jpg')