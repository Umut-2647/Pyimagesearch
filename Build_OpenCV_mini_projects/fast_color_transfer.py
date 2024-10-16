import numpy as np
import cv2


def color_transfer(source,target):
    #görüntüleri RGB'den L*ab* renk uzayına dönüştürün, 
    # kayan nokta veri türünü kullandığınızdan # emin olun 
    # (not: OpenCV # kayan noktaların 32 bit olmasını bekler, bu nedenle 64 bit yerine bunu kullanın)
    source=cv2.cvtColor(source,cv2.COLOR_BAYER_BGR2LAB).astype("float32")
    target=cv2.cvtColor(target,cv2.COLOR_BAYER_BGR2LAB).astype("float32")

    # kaynak ve hedef görüntüler için renk istatistiklerini hesaplayın

    (lMeanSrc,lStdSrc,aMeanSrc,aStdSrc,bMeanSrc,bStdSrc)= image_stats(source)
    (lMeanTar,lStdTar,aMeanTar,aStdTar,bMeanTar,bStdTar)= image_stats(target)

    # hedef görüntüden ortalamaları çıkarın
    (l,a,b)=cv2.split(target)
    l-=lMeanTar
    a-=aMeanTar
    b-=bMeanTar

    # standart sapmalara göre ölçeklendirin
    l=(lStdTar/lStdSrc)*l
    a=(aStdTar/aStdSrc)*a
    b=(bStdTar/bStdSrc)*b

    # kaynak ortalamasını ekleyin

    l+=lMeanSrc
    a+=aMeanSrc
    b+=bMeanSrc
    #piksel yoğunlukları bu aralığın # dışındaysa [0, 255] değerine kırpın
    l=np.clip(l,0,255)
    a=np.clip(a,0,255)
    b=np.clip(b,0,255)

    # kanalları birleştirin ve 8 bitlik işaretsiz tamsayı veri 
    # # türünü kullandığınızdan emin olarak RGB renk 
    # uzayına geri dönüştürün

    transfer=cv2.merge([l,a,b])
    transfer=cv2.cvtColor(transfer.astype("uint8"),cv2.COLOR_LAB2BGR)

    # transfer görüntüsünü geri döndürün
    return transfer

    
    

def image_stats(image):
    # compute the mean and standard deviation of each channel
    (l, a, b) = cv2.split(image)
    (lMean, lStd) = (l.mean(), l.std())
    (aMean, aStd) = (a.mean(), a.std())
    (bMean, bStd) = (b.mean(), b.std())
    return (lMean, lStd, aMean, aStd, bMean, bStd)

