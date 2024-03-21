import cv2
import imutils

img=cv2.imread("C:\\Users\\umuty\\Desktop\\PyImagesearch\\Pyimagesearch\\Learn_OpenCV\\media\\opencv_tutorial_load_image.jpg")


#gurultuyu azaltmak icin onemli bir adim
blurred=cv2.GaussianBlur(img,(11,11),0)

cv2.imshow("Blurred",blurred)
cv2.waitKey(0)