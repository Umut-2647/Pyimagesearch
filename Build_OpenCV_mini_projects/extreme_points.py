import imutils
import cv2

image=cv2.imread("media\\el.png")
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) #gri tonlama
gray=cv2.GaussianBlur(gray,(3,3),0) #gurultu azaltma

thresh=cv2.threshold(gray,45,255,cv2.THRESH_BINARY)[1]  #esikleme
thresh=cv2.erode(thresh,None,iterations=2) #kirpma
thresh=cv2.dilate(thresh,None,iterations=2) #genisletme

cnts=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #contour bulma
cnts=imutils.grab_contours(cnts) #contourlari al

c=max(cnts,key=cv2.contourArea) #en buyuk contouru al
# kontur boyunca en uç noktaları belirleyin

extleft=tuple(c[c[:,:,0].argmin()][0])
extRight=tuple(c[c[:,:,0].argmax()][0])
extTop=tuple(c[c[:,:,1].argmin()][0])
extBot=tuple(c[c[:,:,1].argmax()][0])
# Nesnenin ana hatlarını çizin, 
# ardından en soldaki kırmızı 
# en sağdaki yeşil, en üstteki mavi ve en alttaki deniz mavisi olmak üzere her bir 
# # uç noktayı çizin

cv2.drawContours(image,[c],-1,(0,255,255),2)
cv2.circle(image,extleft,8,(0,0,255),-1)
cv2.circle(image,extRight,8,(0,255,0),-1)
cv2.circle(image,extTop,8,(255,0,0),-1)
cv2.circle(image,extBot,8,(255,255,0),-1)

cv2.imshow("Image",image)   
cv2.waitKey(0)  

