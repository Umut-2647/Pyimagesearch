from Pyimagesearch.More_Advanced_OpenCV_projects.barcode.simple_barcode_detection  import detect
from imutils.video import VideoStream
import argparse
import time
import cv2

ap=argparse.ArgumentParser()
ap.add_argument("-v","--video",help="path to the video file")
args=vars(ap.parse_args())

if not args.get("video",False): #video yoksa
    vs=VideoStream(src=0).start()
    time.sleep(2.0)
else: #video varsa
    vs=cv2.VideoCapture(args["video"])

while True:
    frame=vs.read()
    frame=cv2.flip(frame,1) #aynalama
    frame=frame[1] if args.get("video",False) else frame #video varsa
    if frame is None: #frame yoksa
        break
    box=detect(frame)
    if box is not None: #kutu varsa
        cv2.drawContours(frame,[box],-1,(0,255,0),3) #konturları çizme
    
    cv2.imshow("frame",frame)
    key=cv2.waitKey(1) & 0xFF #q tuşuna basıldığında çıkış

    if key==ord("q"): 
        break

if not args.get("video",False): #video yoksa
    vs.stop()
else:
    vs.release()

cv2.destroyAllWindows() #pencereleri kapatma
