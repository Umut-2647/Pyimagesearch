from Pyimagesearch.More_Advanced_OpenCV_projects.panorama_geridon.panorama_stitching.panorama import Stitcher
import argparse
import imutils
import cv2

ap=argparse.ArgumentParser()
ap.add_argument("-f","--first",required=True,help="path to the first image") # ilk görüntü yolunu alın
ap.add_argument("-s","--second",required=True,help="path to the second image") # ikinci görüntü yolunu alın

args=vars(ap.parse_args()) 

imageA=cv2.imread(args["first"])  # görüntüleri yükleyin
imageB=cv2.imread(args["second"])

imageA=imutils.resize(imageA,width=400) # görüntüleri yeniden boyutlandırın
imageB=imutils.resize(imageB,width=400)

# panorama oluşturmak için görüntüleri birleştirin
stitcher=Stitcher()
(result,vis)=stitcher.stitch([imageA,imageB],showMatches=True)

cv2.imshow("Image A",imageA) # görüntüleri gösterin
cv2.imshow("Image B",imageB)
cv2.imshow("Keypoint Matches",vis)
cv2.imshow("Result",result)
cv2.waitKey(0)


