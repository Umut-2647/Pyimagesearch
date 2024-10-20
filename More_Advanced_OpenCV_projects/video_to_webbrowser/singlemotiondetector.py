import cv2
import numpy as np
import imutils

class SimpleMotionDetector:
    def __init__(self,accumWeight=0.5): #birikim ağırlığı
        self.accumWeight=accumWeight #birikim ağırlığı
        self.bg=None #arka plan
    
    def update(self,image): #arka plan yoksa oluşturma
        if self.bg is None:
            self.bg=image.copy().astype("float")
            return
        # ağırlıklı ortalamayı biriktirerek 
        # arka plan modelini güncelleyin
        cv2.accumulateWeighted(image,self.bg,self.accumWeight)
    
    def detect(self,image,tVal=25):
        # arka plan modeli ile geçirilen görüntü 
        # arasındaki mutlak farkı hesapla # 
        # ardından delta görüntüsünün eşik değerini belirle
        delta=cv2.absdiff(self.bg.astype("uint8"),image) #mutlak fark
        thresh=cv2.threshold(delta,tVal,255,cv2.THRESH_BINARY)[1] #eşikleme
        #kucuk lekeleri kaldırmak icin ufak işlemler
        thresh=cv2.erode(thresh,None,iterations=2)
        thresh=cv2.dilate(thresh,None,iterations=2)
        cnts=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,
                              cv2.CHAIN_APPROX_SIMPLE)
        cnts=imutils.grab_contours(cnts) #kenarları yakalama
        (minX,minY)=(np.inf,np.inf) #en küçük x ve y
        (maxX,maxY)=(-np.inf,-np.inf) #en büyük x ve y
        if len(cnts)==0:
            return None
        for c in cnts:
            # konturun sınırlayıcı kutusunu hesapla 
            # ve bunu # minimum ve maksimum sınırlayıcı 
            # kutu bölgelerini güncellemek için kullan
            (x,y,w,h)=cv2.boundingRect(c)  
            (minX,minY)=(min(minX,x),min(minY,y))  
            (maxX,maxY)=(max(maxX,x+w),max(maxY,y+h))
        return (thresh,(minX,minY,maxX,maxY)) #eşikleme ve sınırlayıcı kutu
    
