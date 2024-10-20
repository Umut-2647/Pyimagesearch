from Pyimagesearch.More_Advanced_OpenCV_projects.save_events.keyclipwriter import KeyClipWriter
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2


ap=argparse.ArgumentParser()
ap.add_argument("-o","--output",required=True,
                help="path to output video file")

ap.add_argument("-p","--picamera",type=int,default=-1,
                help="whether or not the Raspberry Pi camera should be used")

ap.add_argument("-f","--fps",type=int,default=20,
                help="FPS of output video")

ap.add_argument("-c","--codec",type=str,default="MJPG",
                help="codec of output video")

ap.add_argument("-b","--buffer-size",type=int,default=32,
                help="buffer size of video clip writer")

args=vars(ap.parse_args())

print("[INFO] warming up camera...") #kamera ısınıyor
vs=VideoStream(usePiCamera=args["picamera"]>0).start() #kamerayı başlat
time.sleep(2.0) #kamera ısınana kadar bekle

blackLower=(0,0,0) #renk aralıkları
blackUpper=(180,255,30)


kcw=KeyClipWriter(bufSize=args["buffer_size"]) #keyclipwriter sınıfını başlat
consecFrames=0

while True:
    frame=vs.read() #kameradan bir frame oku
    frame=cv2.flip(frame,1)

    frame=imutils.resize(frame,width=600) #frameyi yeniden boyutlandır
    updateConsecFrames=True #frame sayısını güncelle
 
    blurred=cv2.GaussianBlur(frame,(11,11),0) #frameyi bulanıklaştır
    hsv=cv2.cvtColor(blurred,cv2.COLOR_BGR2HSV) #frameyi hsv formatına dönüştür

    mask=cv2.inRange(hsv,blackLower,blackUpper) #maske oluştur
    mask=cv2.erode(mask,None,iterations=2)  #maskeyi erode et 
    mask=cv2.dilate(mask,None,iterations=2) #maskeyi genişlet

    cnts=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,
                          cv2.CHAIN_APPROX_SIMPLE) #maske üzerindeki konturları bul
    cnts=imutils.grab_contours(cnts) #konturları al
    if len(cnts)>0:
        c=max(cnts,key=cv2.contourArea) #en büyük konturu al
        ((x,y),radius)=cv2.minEnclosingCircle(c) #konturu çevreleyen daireyi al
        updateConsecFrames=radius<=10 #eğer yarıçap 10 dan küçükse frame sayısını güncelleme
        if radius>10: #eğer yarıçap 10 dan büyükse
            consecFrames=0 
            cv2.circle(frame,(int(x),int(y)),int(radius), #daireyi çiz
                       (0,255,255),2)
            if not kcw.recording: #kayıt yapılmıyorsa
                timestamp=datetime.datetime.now() #zaman damgası al
                p="{}.avi".format(args["output"],
                                  timestamp.strftime("%Y%m%d-%H%M%S")) #video adı oluştur
                kcw.start(p,cv2.VideoWriter_fourcc(*args["codec"]), #kaydı başlat
                          args["fps"])
    if updateConsecFrames: #frame sayısını güncelle
        consecFrames+=1 
    kcw.update(frame) #frameyi kayıt et
    if kcw.recording and consecFrames==args["buffer_size"]: #eğer frame sayısı buffer size a eşitse
        kcw.finish() #kaydı bitir
        print("[INFO] saved {}".format(p)) 
        
    cv2.imshow("Frame",frame) #frameyi göster
    key=cv2.waitKey(1)&0xFF

    if key==ord("q"):
        break

if kcw.recording:
    kcw.finish()

cv2.destroyAllWindows()
vs.stop()
