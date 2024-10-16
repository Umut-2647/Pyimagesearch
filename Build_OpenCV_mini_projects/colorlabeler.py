from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import cv2

class ColorLabeler:
    def __init__(self):
        colors=OrderedDict({
            "red":(255,0,0),
            "green":(0,255,255),
            "blue":(0,0,255)

        })
        self.lab=np.zeros((len(colors),1,3),dtype="uint8")
        self.colorNames=[]

        for (i,(name,rgb)) in enumerate(colors.items()):
            self.lab[i]=rgb
            self.colorNames.append(name)

            #convert the L*a*b* array from the RGB color space
		    # to L*a*b*
            self.lab=cv2.cvtColor(self.lab,cv2.COLOR_BGR2LAB)

    def label(self,image,c):
        # kontur için bir maske oluşturun, 
        # ardından maskelenmiş bölge için 
        # ortalama L*a*b* değerini hesaplayın
        mask=np.zeros(image.shape[:2],dtype="uint8") #maske olusturuyoruz
        cv2.drawContours(mask,[c],-1,255,-1) #konturun icini dolduruyoruz
        mask=cv2.erode(mask,None,iterations=2) #maskeyi erode ediyoruz
        mean=cv2.mean(image,mask=mask)[:3] #maske icindeki ortalama degeri buluyoruz

        minDist=(np.inf,None) #en kucuk mesafeyi bulmak icin

        for (i,row) in enumerate(self.lab):
            d=dist.euclidean(row[0],mean) #euclidean distance hesapliyoruz

            if d<minDist[0]: #eger distance minDist'ten kucukse
                minDist=(d,i) #minDist'i guncelliyoruz
        
        return self.colorNames[minDist[1]] #en yakin rengi donduruyoruz

