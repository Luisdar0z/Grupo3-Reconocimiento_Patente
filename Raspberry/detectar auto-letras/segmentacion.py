import cv2
import numpy as np

image = cv2.imread('nombre1.jpg')
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(gray,127,255,0)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
areas = [cv2.contourArea(c) for c in contours]
cnt=contours[0]
x,y,w,h = cv2.boundingRect(cnt)
cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
cv2.imshow("Show",image)
cv2.imwrite("nombre3.jpg", image)
cv2.waitKey(0)
