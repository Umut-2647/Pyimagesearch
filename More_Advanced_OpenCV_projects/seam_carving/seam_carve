import cv2
import numpy as np


def seam_carve(image, target_height, target_width):
    # Görüntünün boyutlarını al
    orig_height, orig_width = image.shape[:2]
    
    # Enerji haritasını hesapla
    energy = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    energy = cv2.Sobel(energy, cv2.CV_64F, 1, 1, ksize=3)
    energy = np.abs(energy)

    # Dinamik programlama ile en düşük enerji yolunu bul
    
    # Yeni boyutlandırma işlemini gerçekleştir
    carved_image = cv2.resize(image, (target_width, target_height))

    return carved_image




image = cv2.imread(r"C:\Users\umuty\Desktop\PyImagesearch\Pyimagesearch\More_Advanced_OpenCV_projects\media\seam_carving_example_resize.jpg")

# Hedef boyutları belirle
target_width = 300
target_height = 200

# Seam carving uygula
result = seam_carve(image, target_height, target_width)

# Sonucu göster
cv2.imshow('Seam Carved Image', result)
cv2.imshow("Original",image)
cv2.waitKey(0)
cv2.destroyAllWindows()