import numpy as np
import argparse
import imutils
import cv2

ap=argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,
                help="path to the image file")
args=vars(ap.parse_args())

# görüntüyü diskten yükleyin, gri tonlamaya dönüştürün, bulanıklaştırın 
# ve hapın dış hatlarını ortaya çıkarmak için kenar algılama uygulayın

image=cv2.imread(args["image"])
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
gray=cv2.GaussianBlur(gray,(3,3),0)
edged=cv2.Canny(gray,20,100)

#konturları bulalım

cnts=cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts=imutils.grab_contours(cnts)

if len(cnts)>0:
    # en büyük konturu alın, ardından hap için bir maske çizin
    c=max(cnts,key=cv2.contourArea)
    mask=np.zeros(gray.shape,dtype="uint8")
    cv2.drawContours(mask,[c],-1,255,-1)
    # hapın sınırlayıcı kutusunu hesaplayın, ardından ROI'yi çıkarın 
    # ve maskeyi uygulayın
    (x,y,w,h)=cv2.boundingRect(c)
    imageRoi=image[y:y+h,x:x+w]
    maskRoi=mask[y:y+h,x:x+w]
    imageRoi=cv2.bitwise_and(imageRoi,imageRoi,mask=maskRoi)



for angle in np.arange(0, 360, 15):
	rotated = imutils.rotate(imageRoi, angle)
	cv2.imshow("Rotated (Problematic)", rotated)
	cv2.waitKey(0)
	
for angle in np.arange(0, 360, 15):
	rotated = imutils.rotate_bound(imageRoi, angle)
	cv2.imshow("Rotated (Correct)", rotated)
	cv2.waitKey(0)




