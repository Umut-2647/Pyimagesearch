import cv2
import imutils

img=cv2.imread("C:\\Users\\umuty\\Desktop\\PyImagesearch\\Pyimagesearch\\Learn_OpenCV\\media\\opencv_tutorial_load_image.jpg")

(h,w,d)=img.shape


# önce OpenCV kullanarak bir görüntüyü saat yönünde(-) 45 derece döndürelim
#goruntuyu merkez noktasindan dondurebilmek icin oncelikle merkez noktasini buluyoruz
center=(w//2,h//2)
M=cv2.getRotationMatrix2D(center,-45,1)
rotated=cv2.warpAffine(img,M,(w,h))

# rotasyon imutils aracılığıyla daha az kodla da kolayca gerçekleştirilebilir
rotated2=imutils.rotate(img,-45)    

#kırpılıp kırpılmadıgına gore
rotated3=imutils.rotate_bound(img,45)

cv2.imshow("Imutils Bound Rotation",rotated3)
cv2.imshow("Imutils Rotated",rotated2)
cv2.imshow("OpenCV Rotated",rotated)
cv2.waitKey(0)