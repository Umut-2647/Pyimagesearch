import argparse
import imutils
import cv2


ap=argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,
                help="path to the input image")
args=vars(ap.parse_args())

image=cv2.imread(args["image"])

#resmi gri tonlara ceviriyoruz
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
thresh=cv2.threshold(gray,225,255,cv2.THRESH_BINARY_INV)[1]

mask=thresh.copy()
mask=cv2.erode(mask,None,iterations=5)

mask2=thresh.copy()
mask2=cv2.dilate(mask2,None,iterations=5)


cv2.imshow("Eroded",mask)
cv2.imshow("Dilated",mask2)
cv2.waitKey(0)
