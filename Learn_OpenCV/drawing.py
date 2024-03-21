import cv2
import imutils

img=cv2.imread("C:\\Users\\umuty\\Desktop\\PyImagesearch\\Pyimagesearch\\Learn_OpenCV\\media\\opencv_tutorial_load_image.jpg")

output=img.copy()
#(x1,y1),(x2,y2)

# yüzü çevreleyen 2px kalınlığında kırmızı bir dikdörtgen çizin

cv2.rectangle(output,(290,40),(400,180),(0,0,255),2)
cv2.circle(output,(300,150),20,(255,0,0),-1)
cv2.line(output,(60,20),(400,200),(0,0,255),5)
cv2.putText(output,"OpenCV + Jurassic Park!!!",(10,25),
            cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)



cv2.imshow("Text",output)
cv2.imshow("Line",output)
cv2.imshow("Circle",output)
cv2.imshow("Rectangle",output)
cv2.waitKey(0)