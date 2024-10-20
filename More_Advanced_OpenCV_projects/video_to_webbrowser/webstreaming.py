from Pyimagesearch.More_Advanced_OpenCV_projects.video_to_webbrowser.singlemotiondetector import SimpleMotionDetector
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse 
import datetime
import imutils
import time
import cv2

outputFrame=None
lock=threading.Lock() #kilitleme

app=Flask(__name__) #bir flask uygulaması oluştur

vs=VideoStream(src=0).start() #video akışı başlat
time.sleep(2.0) #kamera ısınması için bekle

@app.route("/")
def index():
    return render_template("index.html")

def detect_motion(frameCount):
    global vs,outputFrame,lock #global değişkenler
    md=SimpleMotionDetector(accumWeight=0.1)
    total=0 #toplam
    while True:
        frame=vs.read() #video akışından bir frame al
        frame=imutils.resize(frame,width=400) #boyutlandırma
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #gri tonlama
        gray=cv2.GaussianBlur(gray,(7,7),0) #bulanıklaştırma
        timestamp=datetime.datetime.now() #zaman damgası
        cv2.putText(frame,timestamp.strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10,frame.shape[0]-10),cv2.FONT_HERSHEY_SIMPLEX,0.35,(0,0,255),1)
        # toplam çerçeve sayısı makul bir arka plan modeli 
        # oluşturmak için yeterli # sayıya ulaştıysa, 
        # # çerçeveyi işlemeye devam edin
        if total>frameCount:
            motion=md.detect(gray)
            if motion is not None: #hareket varsa
                (thresh,(minX,minY,maxX,maxY))=motion
                cv2.rectangle(frame,(minX,minY),(maxX,maxY),
                              (0,0,255),2)
        # arka plan modelini güncelle
        md.update(gray)
        total+=1 #toplamı arttır
        with lock: #kilitleme
            outputFrame=frame.copy() #çerçeveyi kopyala
def generate():
    global outputFrame,lock #global degisken

    while True: 
        with lock: #kilitleme
            if outputFrame is None: #çerçeve yoksa
                continue
            (flag,encodedImage)=cv2.imencode(".jpg",outputFrame)

            if not flag:
                continue
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
              bytearray(encodedImage)+ b'\r\n')
        
@app.route("/video_feed")
def video_feed():
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("-i","--ip",type=str,required=True,
                    help="ip address of the device")
    ap.add_argument("-o","--port",type=int,required=True,
                    help="port number of the server (1024 to 65535)")
    ap.add_argument("-f","--frame-count",type=int,default=32,
                    help="# of frames used to construct the background model")
    args=vars(ap.parse_args())

    t=threading.Thread(target=detect_motion,args=
                       (args["frame_count"],))
    t.daemon=True
    t.start()

    app.run(host=args["ip"],port=args["port"],debug=True,
            threaded=True,use_reloader=False)

vs.stop() #video akışını durdur