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

#225'ten küçük tüm piksel değerlerini ayarlayarak görüntüyü eşikleyin
# ila 255 (beyaz; ön plan) ve tüm piksel değerleri >= 225 ila 255
# (siyah; arka plan), böylece görüntüyü böler

thresh=cv2.threshold(gray,225,255,cv2.THRESH_BINARY_INV)[1]

cv2.imshow("Thresh",thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()