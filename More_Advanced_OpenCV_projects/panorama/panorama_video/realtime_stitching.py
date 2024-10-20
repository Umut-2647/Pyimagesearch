from __future__ import print_function
from Pyimagesearch.More_Advanced_OpenCV_projects.panorama_geridon.panorama_video.panorama_update import Stitcher
from imutils.video import VideoStream
import numpy as np
import datetime
import imutils
import time
import cv2

print("[INFo] starting cameras..")
leftStream=VideoStream(src=0).start()
rightStream=VideoStream(usePiCamera=True).start()

time.sleep(2.0)
