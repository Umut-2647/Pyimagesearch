import cv2
import argparse
import numpy as np
from skimage.exposure import rescale_intensity
import math

def convolve(image,kernel):
    #goruntunun boyutlari
    (IH,IW)=image.shape[:2]
    (KH,KW)=image.shape[:2]
    pad=(KW-1)//2

    image=cv2.copyMakeBorder(image,pad,pad,pad,pad,cv2.BORDER_REPLICATE)
    output=np.zeros((IH,IW),dtype="float32")

#giriş görüntüsü üzerinde döngü yaparak çekirdeği "kaydırır"
# her (x, y)-koordinatı soldan sağa ve yukarıdan aşağıya

    for y in np.arange(pad,IH+pad):
        for x in np.arange(pad,IW+pad):
            #çıkararak görüntünün ROI'sini çıkarır.
            # geçerli (x, y)-koordinatlarının *merkez* bölgesi
            roi=image[y-pad:y+pad+1,x-pad:x+pad+1]
            # ROI ile arasında eleman bazında çarpma
            # çekirdek, sonra matrisin toplanması
            k=(roi*kernel).sum()
            # dönüştürülmüş değeri çıkışta saklayın (x,y)-
            output[y-pad,x-pad]=k
            # çıktı görüntüsünü [0, 255] aralığında olacak şekilde yeniden ölçeklendirin
        output=rescale_intensity(output,in_range=(0,255))
        output=(output*255).astype("uint8")
        return output


ap=argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,
                help="path to the input image")
args=vars(ap.parse_args())
# bir görüntüyü yumuşatmak için kullanılan ortalama bulanıklaştırma çekirdeklerini oluşturun

smallBlur=np.ones((7,7),dtype="float")*(1.0/(7*7))
largeBlur=np.ones((21,21),dtype="float")*(1.0/(21*21))

# bir keskinleştirme filtresi oluşturun

sharpen=np.array((
    [0,-1,0],
    [-1,5,-1],
    [0,-1,0]),dtype="int")

# kenar benzeri algılamak için kullanılan Laplacian çekirdeğini oluşturun

laplacian=np.array((
    [0,1,0],
    [1,-4,1],
    [0,1,0]),dtype="int")

# Sobel x ekseni çekirdeğini oluşturun

sobelX=np.array((
    [-1,0,1],
    [-2,0,2],
    [-1,0,1]),dtype="int")


# Sobel y ekseni çekirdeğini oluşturun

sobelY=np.array((
    [-1,-2,-1],
    [0,0,0],
    [1,2,1]),dtype="int")

# çekirdek bankasını oluşturun, gideceğimiz çekirdeklerin bir listesi
# hem özel `convole` fonksiyonumuzu hem de
# OpenCV'nin `filter2D` işlevi

kernelbank=(
    ("small_blur",smallBlur),
    ("large_blur",largeBlur),
    ("sharpen",sharpen),
    ("laplacian",laplacian),
    ("sobel_x",sobelX),
    ("sobel_y",sobelY)
)

image=cv2.imread(args["image"])
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

for (kernelName,kernel) in kernelbank:
    print("[INFO] applying {} kernel".format(kernelName))
    convoleOutput=convolve(gray,kernel)
    opencvOutput=cv2.filter2D(gray,-1,kernel)

cv2.imshow("Original",gray)
cv2.imshow("{} - convole".format(kernelName),convoleOutput)
cv2.imshow("{} - opencv".format(kernelName),opencvOutput)
cv2.waitKey(0)
cv2.destroyAllWindows()