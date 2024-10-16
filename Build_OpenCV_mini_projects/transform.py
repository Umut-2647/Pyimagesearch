import numpy as np
import cv2

def order_points(pts):
    #ilk sol üst, sonra sağ üst, sonra sağ alt, sonra sol alt
    rect=np.zeros((4,2),dtype="float32")
    #sol üst en küçük toplam, sağ alt en büyük toplam
    s=pts.sum(axis=1)
    rect[0]=pts[np.argmin(s)]
    rect[2]=pts[np.argmax(s)]
    #şimdi noktalar arasındaki farka bakalım
    #sol alt en küçük fark, sağ üst en büyük fark

    diff=np.diff(pts,axis=1)
    rect[1]=pts[np.argmin(diff)]
    rect[3]=pts[np.argmax(diff)]

    return rect

def four_point_transform(image,pts):
    rect=order_points(pts)
    (tl,tr,br,bl)=rect
    #x koordinatlari sağ alt ve sol alt arasındaki max mesafe veya sağ üst ve sol üst arasındaki max mesafe
    widthA=np.sqrt(((br[0]-bl[0])**2)+((br[1]-bl[1])**2))
    widthB=np.sqrt(((tr[0]-tl[0])**2)+((tr[1]-tl[1])**2))
    maxWidth=max(int(widthA),int(widthB))

    #y koordinatlari sağ üst ve sağ alt arasındaki max mesafe veya sol üst ve sol alt arasındaki max mesafe

    heightA=np.sqrt(((tr[0]-br[0])**2)+((tr[1]-br[1])**2))
    heightB=np.sqrt(((tl[0]-bl[0])**2)+((tl[1]-bl[1])**2))
    maxHeight=max(int(heightA),int(heightB))

    #hedef noktalar kümesini oluşturun, yine noktaları # sol üst, sağ üst, sağ alt ve sol alt # sırayla belirleyin
    dst=np.array([
        [0,0],
        [maxWidth-1,0],
        [maxWidth-1,maxHeight-1],
        [0,maxHeight-1]],dtype="float32")
    # perspektif dönüşüm matrisini hesaplayın ve ardından uygulayın
    M=cv2.getPerspectiveTransform(rect,dst) #rect: orjinal noktalar, dst: donusturulmus hedef noktalar
    warped=cv2.warpPerspective(image,M,(maxWidth,maxHeight))

    return warped

