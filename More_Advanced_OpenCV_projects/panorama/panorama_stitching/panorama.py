import numpy as np
import imutils
import cv2

class Stitcher:
    def __init__(self):

        self.isv3=imutils.is_cv3(or_better=True)

    def stitch(self,images,ratio=0.75,reprojThresh=4.0,showMatches=False):

        # görüntüleri paketinden çıkarın, ardından anahtar noktaları tespit edin 
        # ve bunlardan # yerel değişmez tanımlayıcıları çıkarın

        (imageB,imageA)=images
        (kpsA,featuresA)=self.detectAndDescribe(imageA) 
        (kpsB,featuresB)=self.detectAndDescribe(imageB)

        # iki görüntü arasındaki özellikleri eşleştirin
        M=self.matchKeypoints(kpsA,kpsB,featuresA,featuresB,ratio,reprojThresh) # anahtar noktaları eşleştir

        if M is None:
            return None
        
        (matches,H,status)=M # eşleşmeler, homografi matrisi ve durum

        result=cv2.warpPerspective(imageA,H,(imageA.shape[1]+imageB.shape[1],imageA.shape[0])) # görüntüleri birleştirin
        result[0:imageB.shape[0],0:imageB.shape[1]]=imageB

        # anahtar nokta eşleşmelerinin görselleştirilip görselleştirilmeyeceğini kontrol edin

        if showMatches:
            vis=self.drawMatches(imageA,imageB,kpsA,kpsB,matches,status) # eşleşmeleri çiz
            return(result,vis)
        
        return result
    
    def detectAndDescribe(self,image):
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

        # görüntüden özellikleri tespit edin ve çıkarın
        if self.isv3:
            descriptor=cv2.xfeatures2d.SIFT_create() # SIFT tanımlayıcıyı başlatın
            (kps,features)=descriptor.detectAndCompute(image,None) # anahtar noktaları ve özellikleri tespit edin

        else:
            detector=cv2.FeatureDetector_create("SIFT") # SIFT algılayıcıyı başlatın
            kps=detector.detect(gray)   

            #ozellikleri goruntuden cıkarin
            extractor=cv2.DescriptorExtractor_create("SIFT") # SIFT çıkarıcıyı başlatın
            (kps,features)=extractor.compute(gray,kps)  # anahtar noktaları ve özellikleri tespit edin
        
        kps=np.float32([kp.pt for kp in kps])    # anahtar noktaları dönüştürün

        return (kps,features)
    
    def matchKeypoints(self,kpsA,kpsB,featuresA,featuresB,ratio,reprojThresh): # anahtar noktaları eşleştir

        matcher=cv2.DescriptorMatcher_create("BruteForce") # BruteForce eşleştiriciyi başlatın
        rawMatches=matcher.knnMatch(featuresA,featuresB,2) # iki en iyi eşleşmeyi bulun
        matches=[]

        for m in rawMatches:
            # mesafenin birbirinin # belirli bir oranı dahilinde olduğundan emin olun (örn. Lowe'un oran testi)

            if len(m)==2 and m[0].distance<m[1].distance*ratio:
                matches.append((m[0].trainIdx,m[0].queryIdx))

        if len(matches)>4:
            ptsA=np.float32([kpsA[i] for (_,i) in matches]) # eşleşen anahtar noktaları alın
            ptsB=np.float32([kpsB[i] for (i,_) in matches]) # eşleşen anahtar noktaları alın
            # iki nokta kümesi arasındaki homografiyi hesapla
            (H,status)=cv2.findHomography(ptsA,ptsB,cv2.RANSAC,reprojThresh) # RANSAC kullanarak

            return (matches,H,status) # eşleşmeler, homografi matrisi ve durum döndürün
        return None
    
    def drawMatches(self,imageA,imageB,kpsA,kpsB,matches,status): 
        (hA,wA)=imageA.shape[:2]
        (hB,wB)=imageB.shape[:2]
        vis=np.zeros((max(hA,hB),wA+wB,3),dtype="uint8")
        vis[0:hA,0:wA]=imageA
        vis[0:hB,wA:]=imageB

        for ((trainIdx,queryIdx),s) in zip(matches,status):
            if s==1:
                ptA=(int(kpsA[queryIdx][0]),int(kpsA[queryIdx][1]))
                ptB=(int(kpsB[trainIdx][0]+wA),int(kpsB[trainIdx][1]))
                cv2.line(vis,ptA,ptB,(0,255,0),1)
        return vis


