from transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils

ap=argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,help="path to the image to be scanned")
args=vars(ap.parse_args())

#resmi yükleyin ve eski yüksekliğin # yeni yüksekliğe oranını hesaplayın, klonlayın ve yeniden boyutlandırın

image=cv2.imread(args["image"])
ratio=image.shape[0]/500.0
orig=image.copy()

image=imutils.resize(image,height=500)
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
gray=cv2.GaussianBlur(gray,(5,5),0)
edged=cv2.Canny(gray,75,200)

print("STEP 1: Edge Detection")
cv2.imshow("Image",image)
cv2.imshow("Edged",edged)
cv2.waitKey(0)
cv2.destroyAllWindows()

#kenar tespiti yapıldıktan sonra, görüntüdeki konturları bulun
cnts=cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts=imutils.grab_contours(cnts)
#konturların en büyük 5 tanesini alın
cnts=sorted(cnts,key=cv2.contourArea,reverse=True)[:5]

for c in cnts:
    #konturlara yaklaşalım
    peri=cv2.arcLength(c,True)
    approx=cv2.approxPolyDP(c,0.02*peri,True)
    #eger yaklaşık 4 nokta bulunduysa, bu bizim kağıdımızdır
    if len(approx)==4:
        screenCnt=approx
        break
print("STEP 2: Find contours of paper")
cv2.drawContours(image,[screenCnt],-1,(0,255,0),2)
cv2.imshow("Outline",image)
cv2.waitKey(0)
cv2.destroyAllWindows()

#dört noktayı sıralayın ve perspektif dönüşüm uygulayın
warped=four_point_transform(orig,screenCnt.reshape(4,2)*ratio)
#siyah beyaz efekti uygulayın
warped=cv2.cvtColor(warped,cv2.COLOR_BGR2GRAY)
T=threshold_local(warped,11,offset=10,method="gaussian")
warped=(warped>T).astype("uint8")*255

print("STEP 3: Apply perspective transform")
cv2.imshow("Original",imutils.resize(orig,height=650))
cv2.imshow("Scanned",imutils.resize(warped,height=650))
cv2.waitKey(0)



