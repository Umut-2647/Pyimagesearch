from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2

DIGITS_LOOKUP = {
    (1, 1, 1, 0, 1, 1, 1): 0,
    (0, 0, 1, 0, 0, 1, 0): 1,
    (1, 0, 1, 1, 1, 1 ,0): 2,
    (1, 0, 1, 1, 0, 1, 1): 3,
    (0, 1, 1, 1, 0, 1, 0): 4,
    (1, 1, 0, 1, 0, 1, 1): 5,
    (1, 1, 0, 1, 1, 1, 1): 6,
    (1, 0, 1, 0, 0, 1, 0): 7,
    (1, 1, 1, 1, 1, 1, 1): 8,
    (1, 1, 1, 1, 0, 1, 1): 9,
}

image = cv2.imread(r"C:\Users\umuty\Desktop\PyImagesearch\Pyimagesearch\More_Advanced_OpenCV_projects\media\example.jpg")

image = imutils.resize(image, height=500) # yeniden boyutlama
gray= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # gri tona dönüştürme
blurred = cv2.GaussianBlur(gray, (5,5), 0) # görüntüdeki gürültüleri azaltmak yumuşatma uygulandı
edged = cv2.Canny(blurred, 50, 200, 255) # kenar haritası çıkarıldı
cv2.imshow("Edged", edged)

# konturları bulundu ve büyükten küçüğe sıralandı
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
displayCnt = None


for c in cnts:
    peri=cv2.arcLength(c,True) #cevre uzunluğu
    approx=cv2.approxPolyDP(c,0.02*peri,True) #kenarları yakalama

    if len(approx)==4:
        displayCnt=approx
        break

    
warped=four_point_transform(gray,displayCnt.reshape(4,2)) #dört noktayı alıp dönüştürme
output=four_point_transform(image,displayCnt.reshape(4,2)) #dört noktayı alıp dönüştürme

cv2.imshow("warped",warped)
cv2.imshow("output",output)

thresh=cv2.threshold(warped,0,255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)[1] #eşikleme
kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(1,5)) #yapılandırma elemanı
thresh=cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel) #açma işlemi

cv2.imshow("Thresh",thresh)
cv2.waitKey(0)


cnts=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,
                      cv2.CHAIN_APPROX_SIMPLE) #kenarları tespit etme
cnts=imutils.grab_contours(cnts) #kenarları yakalama
digitCnts=[]

for c in cnts:
    (x,y,w,h)=cv2.boundingRect(c) #sınırlayıcı kutu
    if w>=15 and (h>=30 and h<=40):
        digitCnts.append(c)
        
digitCnts=contours.sort_contours(digitCnts,
                                 method="left-to-right")[0] #sıralama

digits=[] #rakamlar

for c in digitCnts:
    (x,y,w,h)=cv2.boundingRect(c) #sınırlayıcı kutu
    roi=thresh[y:y+h,x:x+w] #rakamlarin kesilmesi
    (roiH,roiW)=roi.shape
    (dW,dH)=(int(roiW*0.25),int(roiH*0.15)) #genişlik ve yükseklik
    dHC=int(roiH*0.05) #yükseklik
    
    segments=[ 
        ((0,0),(w,dH)), #üst
        ((0,0),(dW,h//2)), #sol üst
        ((w-dW,0),(w,h//2)), #sağ üst
        ((0,(h//2)-dHC),(w,(h//2)+dHC)), #orta
        ((0,h//2),(dW,h)), #sol alt
        ((w-dW,h//2),(w,h)), #sağ alt
        ((0,h-dH),(w,h)) #alt
        ]
    
    on=[0] * len(segments) #rakamlar

    for (i,((xA,yA),(xB,yB))) in enumerate(segments):
        segROI=roi[yA:yB,xA:xB] #kesilmiş rakamlar

        total=cv2.countNonZero(segROI) #toplam
        area=(xB-xA)*(yB-yA)

        # sıfır olmayan piksellerin toplam sayısı 
        # alanın # %50'sinden fazlaysa, 
        # segmenti "açık" olarak işaretleyin

        if total/float(area)>0.5: 
            on[i]=1

    digit=DIGITS_LOOKUP[tuple(on)] #rakami arayin ve goruntuleyin
    digits.append(digit)
    cv2.rectangle(output,(x,y),(x+w,y+h),(0,255,0),1)
    cv2.putText(output,str(digits),(x-10,y-10),
                cv2.FONT_HERSHEY_SIMPLEX,0.65,(0,255,0),2)

print(u"{}{}.{} \u00b0C".format(*digits)) #dereceyi yazdirma
cv2.imshow("Input",image)
cv2.imshow("Output",output)

cv2.waitKey(0)
cv2.destroyAllWindows()


    
