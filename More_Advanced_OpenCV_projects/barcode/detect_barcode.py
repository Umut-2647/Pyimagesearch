import numpy as np
import cv2
import imutils
import argparse

ap=argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,
                help="path to input image")
args=vars(ap.parse_args())

image=cv2.imread(args["image"])
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

ddepth=cv2.CV_32F if imutils.is_cv2() else cv2.CV_32F #derinlik

gradX=cv2.Sobel(gray,ddepth=ddepth,dx=1,dy=0,ksize=-1) #x ekseninde gradyan
gradY=cv2.Sobel(gray,ddepth=ddepth,dx=0,dy=1,ksize=-1) #y ekseninde gradyan

gradient=cv2.subtract(gradX,gradY) #gradyan farkı
gradient=cv2.convertScaleAbs(gradient) #ölçeklendirme

blurred=cv2.blur(gradient,(9,9)) #bulanıklaştırma
(_,thresh)=cv2.threshold(blurred,225,255,cv2.THRESH_BINARY)

kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(21,7)) #yapılandırma elemanı
closed=cv2.morphologyEx(thresh,cv2.MORPH_CLOSE,kernel) #kapama işlemi

#kalan kucuk nesneleri kaldırma
closed=cv2.erode(closed,None,iterations=4) #erozyon beyaz pikselleri
closed=cv2.dilate(closed,None,iterations=4) #genişletme

cnts=cv2.findContours(closed.copy(),cv2.RETR_EXTERNAL,
                      cv2.CHAIN_APPROX_SIMPLE)  #kenarları tespit etme
cnts=imutils.grab_contours(cnts) #kenarları yakalama

c=sorted(cnts,key=cv2.contourArea,reverse=True)[0] #alanlarına göre sıralama

#en buyuk konturun sınırlayıcı kutusu
rect=cv2.minAreaRect(c)
box=cv2.cv.BoxPoints(rect) if imutils.is_cv2() else cv2.boxPoints(rect)
box=np.int0(box)

cv2.drawContours(image,[box],-1,(0,255,0),3)
cv2.imshow("Image",image)
cv2.waitKey(0)