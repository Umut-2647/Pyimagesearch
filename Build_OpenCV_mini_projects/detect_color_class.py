from shapedetector import ShapeDetector
from colorlabeler import ColorLabeler
import imutils
import argparse
import cv2


ap=argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,help="path to the input image")
args=vars(ap.parse_args())

image=cv2.imread(args["image"])
resized=imutils.resize(image,width=300) #resmi yeniden boyutlandir
ratio=image.shape[0]/ float(resized.shape[0]) #oran hesapla

blurred=cv2.GaussianBlur(resized,(5,5),0)   #gurultu azaltma
gray=cv2.cvtColor(blurred,cv2.COLOR_BGR2GRAY)   #gri tonlama
lab= cv2.cvtColor(blurred,cv2.COLOR_BGR2LAB)    #LAB renk uzayina donusturme
thresh=cv2.threshold(gray,60,255,cv2.THRESH_BINARY)[1]

cnts=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #konturleri bul
cnts=imutils.grab_contours(cnts)

sd=ShapeDetector()
cl=ColorLabeler()

for c in cnts:
    # konturun merkezini hesaplayın
    M=cv2.moments(c)
    cX=int((M["m10"]/M["m00"])*ratio) #x koordinati
    cY=int((M["m01"]/M["m00"])*ratio) #y koordinati

    shape=sd.detect(c) #shape'i bul
    color=cl.label(lab,c) #renkleri bul

    c=c.astype("float")
    c*=ratio
    c=c.astype("int")
    text="{} {}".format(color,shape)
    cv2.drawContours(image,[c],-1,(0,255,0),2)
    cv2.putText(image,text,(cX,cY),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2)

    cv2.imshow("Image",image)
    cv2.waitKey(0)



