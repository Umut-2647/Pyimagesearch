import cv2

class ShapeDetector:
    def __init__(self):
        pass
    
    def detect(self,c):
        shape="unindentified" #varsayilan olarak tanimlandi
        peri=cv2.arcLength(c,True) #contourun cevresini buluyoruz
        approx=cv2.approxPolyDP(c,0.04*peri,True) #contourun kose sayisini buluyoruz

        if len(approx)==3:
            shape="ucgen"

        elif(len(approx)==4):
            (x,y,w,h)=cv2.boundingRect(approx)
            ar=w/float(h)
            #eger aspect ratio 1'e cok yakin ise kare
            shape="kare" if ar>=0.95 and ar<=1.05 else "dikdortgen"

        elif len(approx)==5: #5 kose varsa besgen
            shape="besgen"
        else : #diger durumlar icin daire
            shape="daire"

        return shape #shape'i donduruyoruz
    