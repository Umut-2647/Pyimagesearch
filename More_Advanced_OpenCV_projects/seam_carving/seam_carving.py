from skimage import transform
from skimage import filters
import argparse
import cv2

ap=argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,help="path to the input image")
#varsayilan olarak dikey olarak dikiş çıkarımı yapar
#dikey bir goruntu genisligi ayarlarken yatay bir goruntu yuksekligi ayarlar
ap.add_argument("-d","--direction",type=str,default="vertical",help="seam removal direction")
args=vars(ap.parse_args())

image=cv2.imread(args["image"])
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

#sobel gradyan filtresi uygulayarak enerji haritasini hesaplar
mag=filters.sobel(gray.astype("float")) #enerji haritasini hesaplar

cv2.imshow("Original",image)

for numSeams in range(20,140,20): #20den 140a kadar 20s 20s artarak dikiş çıkarımı yapar
    # görüntüden istenen sayıda 
    # # kareyi kaldırarak dikiş oyma işlemini gerçekleştirin 
    carved=transform.seam_carve(image,mag,args["direction"],numSeams)

    print("[INFO] removing {} seams; new size: " 
          "w={}, h={}".format(numSeams,carved.shape[1],carved.shape[0])) #dikiş çıkarımı yaparak yeni boyutu yazdirir
    cv2.imshow("Carved",carved)
    cv2.waitKey(0) #her bir dikiş çıkarımı işleminden sonra bekler
