import cv2
rostroCascade = cv2.CascadeClassifier("car2.xml")
img = cv2.imread("nombre4.jpg", cv2.IMREAD_UNCHANGED)
print('Original Dimensions : ',img.shape)

scale_percent = 20 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
print(dim)
resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

print('Resized Dimensions : ',resized.shape)
cars = rostroCascade.detectMultiScale(resized, 1.1, 50)

for (x, y, w, h) in cars:
    cv2.rectangle(resized, (x, y), (x + w, y + h), (0, 0, 255), 2)
	#cv2.rectangle(imagen, (x, y), (x+w, y+h), (0, 255, 0), 2)

#cv2.imshow("vehiculos", imagen)
cv2.imshow("Resized image", resized)
cv2.waitKey(0)
