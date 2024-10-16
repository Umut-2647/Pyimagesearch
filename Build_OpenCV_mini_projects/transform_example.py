from transform import four_point_transform
import numpy as np
import argparse
import cv2

ap=argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,help="path to the image file")

#görüntünün yukarıdan aşağıya, "kuş bakışı görünümünü" elde etmek istediğimiz bölgesini temsil eden 4 noktadan oluşan bir liste.

ap.add_argument("-c","--coords",required=True,help="comma seperated list of source points")
args=vars(ap.parse_args())

image=cv2.imread(args["image"])
pts=np.array(eval(args["coords"]),dtype="float32")

warped=four_point_transform(image,pts)
cv2.imshow("Original",image)
cv2.imshow("Warped",warped)
cv2.waitKey(0)
