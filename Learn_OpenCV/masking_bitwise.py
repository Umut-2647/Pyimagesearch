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
output=cv2.bitwise_and(image,image,mask=mask)
cv2.imshow("Output",output)
cv2.waitKey(0)
cv2.destroyAllWindows()