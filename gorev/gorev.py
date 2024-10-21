from imutils import paths
import imutils
import cv2
import argparse
import os

dd = os.path.join(os.getcwd(), "gorev","images")
print(dd)
path_list = []

for i,imagePath in enumerate(paths.list_images(dd)):
    print(imagePath)
    img = cv2.imread(imagePath)
    path_list.append(img)

for path in range(1,len(path_list)):

    difference= cv2.absdiff(path_list[0],path_list[path])

    gray_diff= cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    puan = 0

    for i,contour in enumerate(contours):

        if cv2.contourArea(contour) > 50:  # Küçük alanları hariç tut
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(path_list[path], (x, y), (x + w, y + h), (0, 255, 0), 2)
            #puan hesaplamak için
            img_center_y = path_list[path].shape[1] // 2
            img_center_x = path_list[path].shape[0] // 2
            contour_center_y = y + h // 2
            contour_center_x = x + w // 2

            uzaklik = ((img_center_x - contour_center_x) ** 2 + (img_center_y - contour_center_y) ** 2) ** 0.5
            uzaklik = int(uzaklik)
            if uzaklik < 45:
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
            print(f"{i +1} .Uzaklik: ", uzaklik)

            print("Toplam Puan: ", puan)

    cv2.imshow("Image", path_list[path])
    cv2.waitKey(0)  