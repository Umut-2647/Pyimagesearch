import cv2
import argparse
import imutils

# argüman ayrıştırıcısını oluşturun ve argümanları ayrıştırın
ap=argparse.ArgumentParser()
ap.add_argument("-i","--input",required=True,
help="path to input image")
ap.add_argument("-o","--output",required=True,
help="path to output image")
args=vars(ap.parse_args())

# girdi görüntüsünü diskten yükleyin

img=cv2.imread(args["input"])

# görüntüyü gri tonlara dönüştürün, bulanıklaştırın ve threshold uygulayın
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
blurred=cv2.GaussianBlur(gray,(5,5),0)
thresh=cv2.threshold(blurred,60,255,cv2.THRESH_BINARY)[1]

##konturlarını buluyoruz
cnts=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)


# konturlar üzerinde döngü oluşturup bunları resim üzerine çizin
for c in cnts:
    cv2.drawContours(img,[c],-1,(0,0,255),2)

#goruntudeki toplam sekil sayisini verir

text="I found {} total shapes".format(len(cnts))
cv2.putText(img,text,(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)

#cıktıyı yaz
cv2.imwrite(args["output"],img)



