import cv2
import numpy as np

def enhance_license_plate(image):

    sharpened_plate = cv2.GaussianBlur(image, (0, 0), 3)
    sharpened_plate = cv2.addWeighted(image, 1.7, sharpened_plate, -0.4, 5)

    denoised_plate = cv2.medianBlur(sharpened_plate, 5)

    lab = cv2.cvtColor(denoised_plate, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(4, 4))
    enhanced_l = clahe.apply(l)
    enhanced_lab = cv2.merge((enhanced_l, a, b))
    enhanced_plate = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
    # enhanced_plate = cv2.resize(enhanced_plate, (400,100))

    return enhanced_plate

# plate_image = cv2.imread(r'MainPlate.jpg')
# plate_image = cv2.resize(plate_image, (400,100))
# enhanced_plate_image = enhance_license_plate(plate_image)

# cv2.imshow('Original License Plate', plate_image)
# cv2.imshow('Enhanced License Plate', enhanced_plate_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
