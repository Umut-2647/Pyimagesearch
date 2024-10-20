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
ap.add_argument("-c","--crop",type=int,default=0,
                help="whether to crop out largest rectangular region")
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

    # birleştirilmiş görüntüden en büyük dikdörtgen # 
    # bölgeyi kırpmamız gerekip gerekmediğini kontrol edin
    if args["crop"]>0:
        print("[INFO] cropping...")
        stitched=cv2.copyMakeBorder(stitched,10,10,10,10,cv2.BORDER_CONSTANT,(0,0,0)) #stitched resmin etrafına 10 piksel siyah border eklendi
        gray=cv2.cvtColor(stitched,cv2.COLOR_BGR2GRAY) #stitched resim gray'e dönüştürüldü
        thres=cv2.threshold(gray,0,255,cv2.THRESH_BINARY)[1] #threshold uygulandı

        cnts=cv2.findContours(thres.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #stitiched resimdeki contourlar bulundu
        cnts=imutils.grab_contours(cnts) #contourlar alındı
        c=max(cnts,key=cv2.contourArea) #en büyük contour alındı

        mask=np.zeros(thres.shape,dtype="uint8") #mask oluşturuldu
        (x,y,w,h)=cv2.boundingRect(c)
        cv2.rectangle(mask,(x,y),(x+w,y+h),255,-1) #mask üzerine dikdörtgen çizildi

        # maskenin iki kopyasını oluşturun: biri gerçek # minimum dikdörtgen bölgemiz olarak, 
        # diğeri de minimum # dikdörtgen bölgeyi oluşturmak için kaç pikselin kaldırılması gerektiğine dair 
        # # bir sayaç olarak kullanılmak üzere

        minRect=mask.copy()
        sub=mask.copy()

        while cv2.countNonZero(sub)>0: #sub maskesindeki siyah piksel sayısı 0 olana kadar dön
            minRect=cv2.erode(minRect,None) #minRect maskesi erode edildi
            sub=cv2.subtract(minRect,sub) #sub maskesi minRect maskesinden çıkarıldı

        cnts=cv2.findContours(minRect.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #minRect maskesindeki contourlar bulundu
        cnts=imutils.grab_contours(cnts) #contourlar alındı
        c=max(cnts,key=cv2.contourArea) #en büyük contour alındı

        stitched=stitched[y:y+h,x:x+w] #stitched resim crop edildi


    #birlestirilen resim kaydedildi
    cv2.imwrite(args["output"],stitched)
    cv2.imshow("Stitched",stitched) #birleştirilen resim gösterildi
    cv2.waitKey(0)
else:
    print("[INFO] image stitching failed ({})".format(status))
    




