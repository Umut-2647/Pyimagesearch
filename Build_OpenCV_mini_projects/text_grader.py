from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

ap=argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,help="path to the image file")
args=vars(ap.parse_args())

#soru numaralarını ve cevapları içeren anahtar değer çiftini tanımlayın
ANSWER_KEY={0:1,1:4,2:0,3:3,4:1}

image=cv2.imread(args["image"]) #resmi yükle
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) #gri tonlamaya dönüştür
blurred=cv2.GaussianBlur(gray,(5,5),0)  #görüntüyü bulanıklaştır
edged=cv2.Canny(blurred,75,200) #kenar tespiti yap

cnts=cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #konturları bul
cnts=imutils.grab_contours(cnts) #konturları yakala
docCnt=None #belge konturunu başlat

if len(cnts)>0: #en az 1 kontur varsa
    cnts=sorted(cnts,key=cv2.contourArea,reverse=True) #konturları alanlarına göre sırala
    for c in cnts:
        peri=cv2.arcLength(c,True) #konturun çevresini hesapla
        approx=cv2.approxPolyDP(c,0.02*peri,True) #konturu yaklaşıkla

        if len(approx)==4: #eğer yaklaşık 4 kenar varsa
            docCnt=approx
            break

paper=four_point_transform(image,docCnt.reshape(4,2)) #dört noktayı sırala ve perspektif dönüşüm uygula
warped=four_point_transform(gray,docCnt.reshape(4,2)) #hem orijinal resim uzerine hem de gri tonlamali resim

thresh=cv2.threshold(warped,0,255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)[1] #ters gri tonlamali resmi threshold uygula
cnts=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #konturlari bul
cnts=imutils.grab_contours(cnts) #konturlari yakala

questionCnts=[] #soru konturlarini baslat

for c in cnts:
    (x,y,w,h)= cv2.boundingRect(c) #konturun etrafını çerçevele
    ar= w/float(h)
    # konturu bir soru olarak etiketlemek için, bölge 
    # # yeterince geniş, yeterince uzun ve 
    # # yaklaşık olarak 1'e eşit bir en boy oranına sahip olmalıdır

    if w>=20 and h>=20 and ar>=0.9 and ar<=1.1:
        questionCnts.append(c)

questionCnts=contours.sort_contours(questionCnts,method="top-to-bottom")[0] #soruları yukarıdan asagı dogru sırala
correct=0 #dogru sayısını başlat

for (q,i) in enumerate(np.arange(0,len(questionCnts),5)): #her soru icin 5 olası yanit olacagini belirt
    cnts=contours.sort_contours(questionCnts[i:i+5])[0] #soruları soldan saga dogru sırala
    bubbled=None

    for (j,c) in enumerate(cnts):
        mask=np.zeros(thresh.shape,dtype="uint8") #maske olustur
        cv2.drawContours(mask,[c],-1,255,-1) #konturu maskele
        mask=cv2.bitwise_and(thresh,thresh,mask=mask)
        total=cv2.countNonZero(mask) #maskeleme sonucunda sıfır olmayan toplam piksel sayısını hesapla

        if bubbled is None or total>bubbled[0]:
            bubbled=(total,j)
        color=(0,0,255)
        k=ANSWER_KEY[q]
    if k==bubbled[1]:
        color=(0,255,0)
        correct=correct+1
        print(correct)
        
    cv2.drawContours(paper,[cnts[k]],-1,color,3)
    

score=(correct/5.0)*100
print(correct)
print("[INFO] score: {:.2f}%".format(score))
cv2.putText(paper,"{:.2f}%".format(score),(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,0,255),2)
cv2.imshow("Original",image)
cv2.imshow("Exam",paper)
cv2.waitKey(0)












cv2.imshow("Image",image)
cv2.imshow("Edged",edged)
cv2.waitKey(0)
