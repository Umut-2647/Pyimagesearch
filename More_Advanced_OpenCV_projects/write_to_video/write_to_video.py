from __future__  import print_function
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True,
	help="path to output video file")
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
ap.add_argument("-f", "--fps", type=int, default=20,
	help="FPS of output video")
ap.add_argument("-c", "--codec", type=str, default="MJPG",
	help="codec of output video")
args = vars(ap.parse_args())

print("[INFO] warming up camera")
vs=VideoStream(usePiCamera=args["picamera"]>0).start()
time.sleep(2.0)
fourcc=cv2.VideoWriter_fourcc(*args["codec"])
writer=None
(h,w)=(None,None)
zeros=None

while True:
	frame=vs.read()
	frame=cv2.flip(frame,1)

	frame=imutils.resize(frame,width=300)

	if writer is None:
		(h,w)=frame.shape[:2]
		writer=cv2.VideoWriter(args["output"],fourcc,args["fps"],
		(w*2,h*2),True)
		zeros=np.zeros((h,w),dtype="uint8")
	# görüntüyü RGB bileşenlerine ayırın, ardından # 
	# her karenin RGB temsilini ayrı ayrı oluşturun

	(B,G,R)=cv2.split(frame)
	R=cv2.merge([zeros,zeros,R])
	G=cv2.merge([zeros,G,zeros])
	B=cv2.merge([B,zeros,zeros])
	# Orijinal kareyi # sol üstte, 
	# kırmızı kanalı sağ üstte, 
	# yeşil # kanalı sağ altta ve 
	# mavi kanalı sol altta depolayarak # son çıktı karesini oluşturur
	output=np.zeros((h*2,w*2,3),dtype="uint8")
	output[0:h,0:w]=frame
	output[0:h,w:w*2]=R
	output[h:h*2,w:w*2]=G
	output[h:h*2,0:w]=B

	writer.write(frame)
	cv2.imshow("Frame",frame)
	cv2.imshow("Output",output)
	key=cv2.waitKey(1) & 0XFF

	if key==ord("q"):
		break

print("INFO cleaning up...")
cv2.destroyAllWindows()
vs.stop()
writer.release()


	

