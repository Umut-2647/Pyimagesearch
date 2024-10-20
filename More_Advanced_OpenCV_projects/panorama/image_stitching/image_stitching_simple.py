from imutils import paths
import numpy as np
import argparse
import imutils
import cv2

ap=argparse.ArgumentParser()
ap.add_argument("-i","--images",type=str,required=True,
    help="path to input directory of images to stitch")
ap.add_argument("-o","--output",type=str,required=True,
                help="path to the output image")
args=vars(ap.parse_args())

print("[INFO] loading images...")
imagePaths=sorted(list(paths.list_images(args["images"]))) #list_images fonksiyonu ile resimlerin path'leri alındı
images=[]

for imagePath in imagePaths: #resimlerin path'leri üzerinde dönüldü
    image=cv2.imread(imagePath) #resimler okundu
    images.append(image) #resimler images listesine eklendi

print("[INFO] stitching images...")
stitcher=cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create() #stitcher nesnesi oluşturuldu
(status,stitched)=stitcher.stitch(images) #resimler birleştirildi

if status==0: #status 0 ise başarılı birleştirme yapıldı
    
    #birlestirilen resim kaydedildi
    cv2.imwrite(args["output"],stitched) 
    cv2.imshow("Stitched",stitched) #birleştirilen resim gösterildi
    cv2.waitKey(0)

else: #status 0 değilse birleştirme başarısız
    print("[INFO] image stitching failed ({})".format(status))
    
