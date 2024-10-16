import numpy as np
import cv2
import imutils
import argparse

ap=argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,
                help="path to the input image")
args=vars(ap.parse_args())

image=cv2.imread(args["image"])
# görüntüdeki tüm 'siyah' şekilleri bulun

lower=np.array([0,0,0])
upper=np.array([15,15,15]) #siyah rengin aralığı

shapeMask=cv2.inRange(image,lower,upper)

cnts=cv2.findContours(shapeMask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts=imutils.grab_contours(cnts)
print("I found {} black shapes".format(len(cnts)))
cv2.imshow("Mask",shapeMask)

for c in cnts:
    cv2.drawContours(image,[c],-1,(0,255,0),2)
    cv2.imshow("Image",image)
    cv2.waitKey(0)
    
