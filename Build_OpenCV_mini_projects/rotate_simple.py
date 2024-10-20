import numpy as np
import argparse
import imutils
import cv2

ap=argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,
                help="path to the image file")
args=vars(ap.parse_args())

image=cv2.imread(args["image"])

# dönüş açıları üzerinde döngü
for angle in np.arange(0,360,15):
    rotated=imutils.rotate(image,angle)
    cv2.imshow("Rotated (Problematic)",rotated)
    cv2.waitKey(0)

# döndürme açıları üzerinde tekrar döngü yapın, 
# bu sefer # görüntünün hiçbir kısmının kesilmediğinden emin olun

for angle in np.arange(0,360,15):
    rotated=imutils.rotate_bound(image,angle)
    cv2.imshow("Rotated (Correct)",rotated)
    cv2.waitKey(0)
    

