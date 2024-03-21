import imutils
import cv2

# girdi resmini yükleyin ve boyutlarını gösterin, şunu unutmayın

img=cv2.imread("C:\\Users\\umuty\\Desktop\\PyImagesearch\\Pyimagesearch\\Learn_OpenCV\\media\\opencv_tutorial_load_image.jpg")

#ilk yukseklik gelir
(h,w,d)=img.shape

# şekil satır sayısı (yükseklik) x sütun sayısı (genişlik) x kanal sayısı (derinlik)

print("width :{}, height :{}, depth :{}".format(w,h,d))


#x=50, y=100 adresinde bulunan RGB pikseline erişiyoruz

# OpenCV görüntüleri RGB yerine BGR sırasına göre saklar

(B,G,R)=img[100,50]
print("R :{}, G:{}, B :{}".format(R,G,B))

#image[startY:endY, startX:endX] 
roi=img[50:180,320:420]
resized=cv2.resize(img,(200,200))

# 300px olacak, ancak yeni yüksekliği en boy oranına göre hesaplayacak
#en boy oranini dikkate alarak goruntu bozulmadan yeniden boyutlandirma
r=300.0/w
dim=(300,int(h*r))
resized=cv2.resize(img,dim)

#imutils kutuphanesini kullanarak en-boy oranini daha kolay bir sekilde hesaplayabiliriz
resized=imutils.resize(img,width=500)


cv2.imshow("Fixed Resizing",resized)
cv2.imshow("ROI",roi)
cv2.imshow("Image",img)
cv2.waitKey(0)

