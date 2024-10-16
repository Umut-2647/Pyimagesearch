from imutils import build_montages
from imutils import paths
import argparse
import cv2
import random

ap=argparse.ArgumentParser()
ap.add_argument("-i","--images",required=True,
                help="path to input directory of images") 
ap.add_argument("-s","--sample",type="int",default=21,
                help="# of images to sample") #

args=vars(ap.parse_args())

imagePaths=list(paths.list_images(args["images"])) #tüm resimlerin yollarını alır
random.shuffle(imagePaths) #resimleri karıştırır
imagePaths=imagePaths[:args["sample"]] #resimlerden herhangi birini alır

images=[]

#resimleri yükle
for imagePath in imagePaths:
    image=cv2.imread(imagePath)
    images.append(image)

montages=build_montages(images,(128,196),(7,3)) #montajları oluşturur

#montajları döngüye alın ve gösterin
for montage in montages:
    cv2.imshow("Montage",montage)
    cv2.waitKey(0)
