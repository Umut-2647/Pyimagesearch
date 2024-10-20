import argparse
import cv2

ap=argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,help="path to the input image")
args=vars(ap.parse_args())


image=cv2.imread(args["image"])

# OpenCV'nin statik belirginlik spektral kalıntı dedektörünü başlatın ve 
# # belirginlik haritasını hesaplayın

saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
(success,saliencyMap)=saliency.computeSaliency(image)
saliencyMap=(saliencyMap*255).astype("uint8")


cv2.imshow("Image",image)
cv2.imshow("output",saliencyMap)
cv2.waitKey(0)

saliency=cv2.saliency.StaticSaliencyFineGrained_create()
(success,saliencyMap)=saliency.computeSaliency(image)

threshMap=cv2.threshold((saliencyMap*255).astype("uint8"),0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]

cv2.imshow("Image",image)
cv2.imshow("Output",saliencyMap)
cv2.imshow("Thresh",threshMap)
cv2.waitKey(0)



