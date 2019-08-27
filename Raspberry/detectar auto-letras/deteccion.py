"""
import cv2
import numpy

cascade_src = "cars.xml"
car_cascade = cv2.CascadeClassifier(cascade_src)


img1 = cv2.imread("foto1.jpg")
filtro = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

while True:
    ret, img = img1.read()
    if (type(img) == type(None)):
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cars = car_cascade.detectMultiScale(gray, 1.1, 1)

    for (x, y, w, h) in cars:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv2.imshow('video', img)

    if cv2.waitKey(33) == 27:
        break

cv2.imshow('car', img)
"""

import cv2

rostroCascade = cv2.CascadeClassifier("car2.xml")

imagen = cv2.imread("nombre4.jpg")
filtro = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
"""
cars = rostroCascade.detectMultiScale(
	filtro,
	scaleFactor = 1.2,
	minNeighbors = 5,
	minSize= (30,30),
	flags = cv2.CASCADE_SCALE_IMAGE
)
"""
gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
cars = rostroCascade.detectMultiScale(gray, 1.1, 50)

for (x, y, w, h) in cars:
    cv2.rectangle(imagen, (x, y), (x + w, y + h), (0, 0, 255), 2)
	#cv2.rectangle(imagen, (x, y), (x+w, y+h), (0, 255, 0), 2)

cv2.imshow("vehiculos", imagen)
cv2.waitKey(0)
