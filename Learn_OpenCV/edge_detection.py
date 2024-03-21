import argparse
import imutils
import cv2


ap=argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,
                help="path to the input image")
args=vars(ap.parse_args())

image=cv2.imread(args["image"])

#resmi gri tonlara ceviriyoruz(kenar algilama icin)
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

edged=cv2.Canny(gray,30,150)





cv2.imshow("Edged",edged)
cv2.imshow("Gray",gray)
cv2.imshow("Image",image)
cv2.waitKey()