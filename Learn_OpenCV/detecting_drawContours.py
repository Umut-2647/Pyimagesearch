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
#konturlari buluyoruz

cnts=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,
                      cv2.CHAIN_APPROX_SIMPLE)

cnts=imutils.grab_contours(cnts)
output=image.copy()

for c in cnts:
    cv2.drawContours(output,[c],-1,(240,0,159),3)


text="I found {} objects!".format(len(cnts))
cv2.putText(output,text,(10,25),cv2.FONT_HERSHEY_SIMPLEX,
            0.7,(240,0,159),2)

cv2.imshow("Contours",output)
cv2.waitKey(0)
