from imutils.video import VideoStream
import imutils
import time
import cv2

saliency=None
vs=VideoStream(src=0).start()
time.sleep(2.0)

while True:
    frame=vs.read() #framelerimizi okumaya basliyoruz
    frame=cv2.flip(frame,1)
    frame=imutils.resize(frame,width=500) #yeniden boyutlandiriyoruz

    if saliency is None:
        # hareket belirginliği nesnesini, henüz oluşturulmamışsa, örneklendirir
        saliency=cv2.saliency.MotionSaliencyBinWangApr2014_create()
        saliency.setImagesize(frame.shape[1],frame.shape[0])
        saliency.init()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #gri tonlara ceviriyoruz
    (success,saliencyMap)=saliency.computeSaliency(gray)  #belirginlik haritamızı hesaplıyoruz
    
    #SaliencyMap [0, 1] aralığında float değerler içerdiğinden, 
    # [0, 255] aralığına ölçeklendiririz ve değerin işaretsiz 8 bitlik bir tamsayı olmasını sağlarız
    saliencyMap=(saliencyMap*255).astype("uint8")

    cv2.imshow("Frame",frame)
    cv2.imshow("Map",saliencyMap)
    key=cv2.waitKey(1) & 0xFF

    if key==ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()
