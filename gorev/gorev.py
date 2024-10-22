from imutils import paths
import imutils
import cv2
import argparse
import os

dd = os.path.join(os.getcwd(),"Pyimagesearch" ,"gorev","images") #os.getcwd() ile çalıştığımız dizini alıyoruz ve images klasörüne ulaşıyoruz

print(dd) #dd değişkeni ile images klasörünün yolunu yazdırıyoruz

path_list = [] #path_list adında bir liste oluşturuyoruz

for i,imagePath in enumerate(paths.list_images(dd)): #images klasöründeki resimlerin yolunu alıyoruz

    print(imagePath) #resimlerin yolunu yazdırıyoruz
    img = cv2.imread(imagePath) #resimleri okuyoruz   
    path_list.append(img) #resimleri path_list listesine ekliyoruz


for path in range(1,len(path_list)): #path_list listesindeki resimlerin sayısına kadar döngü oluşturuyoruz

    difference= cv2.absdiff(path_list[0],path_list[path]) #İki resim arasındaki farkı alıyoruz

    gray_diff= cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY) #Farkı alınan resmi griye çeviriyoruz
    _, thresh = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY) #Griye çevrilen resmi threshold uyguluyoruz
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #Threshold uygulanan resimdeki konturları buluyoruz
    puan = 0

    for i,contour in enumerate(contours): #Konturların sayısına kadar döngü oluşturuyoruz

        if cv2.contourArea(contour) > 50:  # Küçük alanları hariç tut

            x, y, w, h = cv2.boundingRect(contour) #konturun alanini buluyoruz  

            cv2.rectangle(path_list[path], (x, y), (x + w, y + h), (0, 255, 0), 2) #Konturların etrafına dikdörtgen çiziyoruz
            #puan hesaplamak için
            img_center_y = path_list[path].shape[1] // 2  #resmin x ve y koordinatlarını alıyoruz
            img_center_x = path_list[path].shape[0] // 2
            contour_center_y = y + h // 2   #konturun x ve y koordinatlarını alıyoruz
            contour_center_x = x + w // 2

            #iki nokta arasındaki uzaklığı hesaplıyoruz
            uzaklik = ((img_center_x - contour_center_x) ** 2 + (img_center_y - contour_center_y) ** 2) ** 0.5
            uzaklik = int(uzaklik) 
            if uzaklik < 45: #uzaklık değerine göre puanlama yapıyoruz
                puan += 1
            elif uzaklik > 55 and uzaklik <= 100: 
                puan += 2
            elif uzaklik > 100 and uzaklik <= 160:
                puan += 3
            elif uzaklik > 160 and uzaklik <= 220:
                puan += 4
            elif uzaklik > 220 and uzaklik <= 300:
                puan += 5
            else :
                puan += 0
            print(f"{i +1} .Uzaklik: ", uzaklik) #her atisin merkeze olan uzakligini yazdiriyoruz

            print("Toplam Puan: ", puan)

    cv2.putText(path_list[path], f"Puan: {puan}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2) #Puanı resmin üstüne yazdırıyoruz
    cv2.imshow("Image", path_list[path])
    cv2.waitKey(0)  