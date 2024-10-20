from imutils import paths
import argparse
import cv2

def variance_of_laplacian(image): 
    return cv2.Laplacian(image,cv2.CV_64F).var() #goruntunun laplaciani hesaplayin(bulaniklik miktarini)

ap=argparse.ArgumentParser()
ap.add_argument("-i","--images",required=True,help="path to the image")
ap.add_argument("-t","--threshold",type=float,default=100,
                help="focus measures that fall below this value will be considered 'blurry'")
args=vars(ap.parse_args())
for imagePath in paths.list_images(args["images"]): #resimlerin yollarini alir
    image=cv2.imread(imagePath) #resmi okur
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) #resmi gri tonlara donusturur
    fm=variance_of_laplacian(gray) #gri tonlamali resim uzerinde laplancia methodunu calistirir ve bulaniklik oranini bulur
    text="Not blurry"
    # odak ölçüsü verilen eşikten küçükse, # görüntü "bulanık" olarak kabul edilmelidir
    if fm<args["threshold"]:
        text="Blurry"

    cv2.putText(image,"{}: {:.2f}".format(text,fm),(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255),3)
    cv2.imshow("Image",image)
    key=cv2.waitKey(0)
